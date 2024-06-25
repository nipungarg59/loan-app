from django.db import models

from loans.constants import LOAN_STATE_PENDING


class LoanManager(models.Manager):

    def __init__(self) -> None:
        super().__init__()

    def get_pending_loan_by_id(self, loan_id):
        return self.filter(pk=loan_id, state=LOAN_STATE_PENDING)

