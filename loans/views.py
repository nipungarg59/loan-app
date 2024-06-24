from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from generics.responses.responses import success_response, error_response
from loans.constants import LOAN_STATE_PENDING, LOAN_STATE_APPROVED, LOAN_STATE_PAID
from loans.models import Loan, LoanRepayment
from loans.serializers import LoanSerializer, LoanRepaymentSerializer
from loans.utils import get_loan_repayment_date_and_term
from users.authorisation.admin_role_permission import AdminUserOnly


class CreateLoanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save(user=request.user)
            # Create scheduled repayments
            repayments = [LoanRepayment(loan=loan, repayment_date=repayment_date, amount=repayment_date) for (repayment_date, repayment_date) in get_loan_repayment_date_and_term(loan.amount, loan.term)]
            LoanRepayment.objects.bulk_create(repayments)
            return success_response(LoanSerializer(loan).data, message='Loan created successfully', status_code=201)
        return error_response(serializer.errors, message='Invalid data', status_code=400)


class ApproveLoanAPIView(APIView):
    permission_classes = [IsAuthenticated, AdminUserOnly]

    def post(self, request, loan_id):
        # Update the loan
        loan = get_object_or_404(Loan, id=loan_id, state=LOAN_STATE_PENDING)
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

    def post(self, request, repayment_id):
        repayment = get_object_or_404(LoanRepayment, id=repayment_id, state=LOAN_STATE_PENDING)
        if repayment.loan.user != request.user:
            return error_response('Permission denied', message='You can only repay your own loans', status_code=403)
        amount = request.data.get('amount')
        if amount < repayment.amount:
            return error_response('Invalid amount', message='Repayment amount must be greater than or equal to the scheduled amount', status_code=400)
        repayment.state = LOAN_STATE_PAID
        repayment.save()

        # Check if all repayments are paid
        loan = repayment.loan
        if not LoanRepayment.objects.filter(loan=loan, state=LOAN_STATE_PENDING).exists():
            loan.state = LOAN_STATE_PAID
            loan.save()

        return success_response(LoanRepaymentSerializer(repayment).data, message='Repayment added successfully')
