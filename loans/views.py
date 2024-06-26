import decimal

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from generics.responses.responses import success_response, error_response
from loans.constants import LOAN_STATE_APPROVED, LOAN_STATE_PAID
from loans.models import Loan, LoanRepayment
from loans.serializers import LoanSerializer
from loans.utils import get_loan_repayment_date_and_term, update_pending_repayments
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
            repayments = [LoanRepayment(loan=loan, repayment_date=repayment_date, amount=amount)
                          for (repayment_date, amount) in get_loan_repayment_date_and_term(loan.amount, loan.term)]
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
    """
    This API will list all the user loans and their repayment
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return success_response(serializer.data, message='User loans fetched successfully')


class AddRepaymentAPIView(APIView):
    """
    This API will need the loan_id and repayment amount as input.
    If amount can only pay partially then pending repayment will be updated by partial repayment
    else if amount > repayment amount for single term then repayment will be marked as paid and
    rest amount will be used for paying other repayments if left.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id, user=request.user, state=LOAN_STATE_APPROVED)
        except Exception:
            return error_response({}, message='Either loan is not approved or does not exist', status_code=404)

        pending_repayments = LoanRepayment.objects.get_pending_repayments_by_loan(loan=loan).order_by('repayment_date')

        update_pending_repayments(pending_repayments, decimal.Decimal(request.data.get('amount')))

        # Check if all repayments are paid
        if not LoanRepayment.objects.get_pending_repayments_by_loan(loan=loan).exists():
            loan.state = LOAN_STATE_PAID
            loan.save()

        return success_response(LoanSerializer(loan).data, message='Repayment added successfully')
