from rest_framework import serializers
from loans.models import Loan, LoanRepayment


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ['id', 'loan', 'amount', 'term', 'repayment_date', 'state', 'created_at', 'updated_at']
        read_only_fields = ['state', 'created_at', 'updated_at']


class LoanSerializer(serializers.ModelSerializer):
    repayments = LoanRepaymentSerializer(many=True, read_only=True, source='loanrepayment_set')

    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'term', 'state', 'created_at', 'updated_at', 'repayments']
        read_only_fields = ['state', 'created_at', 'updated_at']
