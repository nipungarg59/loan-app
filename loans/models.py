import decimal

from django.db import models

from generics.models.base_model import BaseModel
from loans.constants import LOAN_STATE_CHOICES, LOAN_STATE_PENDING
from loans.managers import LoanManager, LoanRepaymentManager
from users.models import User


# Create your models here.

class Loan(BaseModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    term = models.IntegerField(blank=False, null=False)
    state = models.CharField(max_length=10, choices=LOAN_STATE_CHOICES, default=LOAN_STATE_PENDING)

    objects = LoanManager()

    def __str__(self):
        return f'Loan {self.id} for {self.user.user_name}'


class LoanRepayment(BaseModel):
    loan = models.ForeignKey(Loan, blank=False, null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=decimal.Decimal(0))
    repayment_date = models.DateTimeField(blank=False, null=False)
    state = models.CharField(max_length=10, choices=LOAN_STATE_CHOICES, default=LOAN_STATE_PENDING)

    objects = LoanRepaymentManager()

    def __str__(self):
        return f'Repayment {self.id} for Loan {self.loan.id}'
