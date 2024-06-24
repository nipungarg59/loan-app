from django.db import models

from generics.models.base_model import BaseModel
from users.models import User


# Create your models here.

class Loan(BaseModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(blank=False, null=False)
    term = models.IntegerField(blank=False, null=False)


class LoanRepayment(BaseModel):
    loan = models.ForeignKey(Loan, blank=False, null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(blank=False, null=False)
    term = models.IntegerField(blank=False, null=False)
    repayment_date = models.DateTimeField(blank=False, null=False)
