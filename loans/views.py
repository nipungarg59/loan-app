import decimal

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from generics.responses.responses import success_response, error_response
from loans.constants import LOAN_STATE_PENDING, LOAN_STATE_APPROVED, LOAN_STATE_PAID
from loans.models import Loan, LoanRepayment
from loans.serializers import LoanSerializer
from loans.utils import get_loan_repayment_date_and_term, get_repayment_amount, is_repayment_complete
from users.authorisation.admin_role_permission import AdminUserOnly


class CreateLoanAPIView(APIView):
    """
    This API is to create the loans for the User
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.pk
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            loan = serializer.save(user=request.user)
            # Create scheduled repayments
            repayments = [LoanRepayment(loan=loan, repayment_date=repayment_date, amount=amount) for (repayment_date, amount) in get_loan_repayment_date_and_term(loan.amount, loan.term)]
            LoanRepayment.objects.bulk_create(repayments)
            return success_response(LoanSerializer(loan).data, message='Loan created successfully', status_code=201)
        return error_response(serializer.errors, message='Invalid data', status_code=400)


class ApproveLoanAPIView(APIView):
    """
    This API is to approve the loan by the admin user
    """
    permission_classes = [IsAuthenticated, AdminUserOnly]

    def put(self, request, loan_id):
        # Update the loan
        loans = Loan.objects.get_pending_loan_by_id(loan_id)
        if not loans.exists():
            return error_response({}, message='Either loan is not in pending state or loan is already approved', status_code=404)
        loan = loans.first()
        loan.state = LOAN_STATE_APPROVED
        loan.save()
        return success_response(LoanSerializer(loan).data, message='Loan approved successfully')


class ListUserLoansAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return success_response(serializer.data, message='User loans fetched successfully')


class AddRepaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id, user=request.user, state=LOAN_STATE_APPROVED)
        except Loan.DoesNotExist:
            raise error_response({}, message='Either loan is not approved or does not exist', status_code=404)

        pending_repayments = LoanRepayment.objects.filter(loan=loan, state=LOAN_STATE_PENDING).order_by('repayment_date')

        total_amount = decimal.Decimal(request.data.get('amount'))
        remaining_amount = total_amount

        for pending_repayment in pending_repayments:
            if remaining_amount == decimal.Decimal(0):
                break
            repayment_amount = get_repayment_amount(pending_repayment, remaining_amount)
            pending_repayment.amount_paid += repayment_amount
            remaining_amount -= repayment_amount
            if is_repayment_complete(pending_repayment):
                pending_repayment.state = LOAN_STATE_PAID
            pending_repayment.save()

        # Check if all repayments are paid
        if not LoanRepayment.objects.filter(loan=loan, state=LOAN_STATE_PENDING).exists():
            loan.state = LOAN_STATE_PAID
            loan.save()

        return success_response(LoanSerializer(loan).data, message='Repayment added successfully')
