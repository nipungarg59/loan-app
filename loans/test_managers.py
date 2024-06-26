from decimal import Decimal
from unittest import TestCase

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from loans.models import Loan, LoanManager, LoanRepayment
from loans.constants import LOAN_STATE_PENDING, LOAN_STATE_APPROVED, LOAN_STATE_PAID
from users.models import User


class LoanManagerTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()
        Loan.objects.all().delete()
        LoanRepayment.objects.all().delete()

        # Create test users
        self.user1 = User.objects.create(
            user_name="user1",
            password=make_password("password1"),
            role="Customer"
        )
        self.user2 = User.objects.create(
            user_name="user2",
            password=make_password("password2"),
            role="Admin"
        )

        # Create test loans
        self.loan1 = Loan.objects.create(
            user=self.user1,
            amount=Decimal('10000.00'),
            term=3,
            state=LOAN_STATE_PENDING
        )
        self.loan2 = Loan.objects.create(
            user=self.user2,
            amount=Decimal('15000.00'),
            term=2,
            state=LOAN_STATE_APPROVED
        )
        self.loan3 = Loan.objects.create(
            user=self.user1,
            amount=Decimal('20000.00'),
            term=4,
            state=LOAN_STATE_PENDING
        )

        # Create test loan repayments
        self.repayment1 = LoanRepayment.objects.create(
            loan=self.loan1,
            amount=Decimal('3333.33'),
            amount_paid=Decimal('3333.33'),
            repayment_date=timezone.now(),
            state=LOAN_STATE_PAID
        )
        self.repayment2 = LoanRepayment.objects.create(
            loan=self.loan1,
            amount=Decimal('3333.33'),
            amount_paid=Decimal('0.00'),
            repayment_date=timezone.now(),
            state=LOAN_STATE_PENDING
        )
        self.repayment3 = LoanRepayment.objects.create(
            loan=self.loan1,
            amount=Decimal('3333.34'),
            amount_paid=Decimal('0.00'),
            repayment_date=timezone.now(),
            state=LOAN_STATE_PENDING
        )
        self.repayment4 = LoanRepayment.objects.create(
            loan=self.loan2,
            amount=Decimal('7500.00'),
            amount_paid=Decimal('7500.00'),
            repayment_date=timezone.now(),
            state=LOAN_STATE_PAID
        )
        self.repayment5 = LoanRepayment.objects.create(
            loan=self.loan2,
            amount=Decimal('7500.00'),
            amount_paid=Decimal('7500.00'),
            repayment_date=timezone.now(),
            state=LOAN_STATE_PAID
        )

    def test_get_pending_loan_by_id(self):
        # Test case where loan with PENDING state exists
        pending_loan = Loan.objects.get_pending_loan_by_id(self.loan1.id)
        self.assertEqual(pending_loan.count(), 1)
        self.assertEqual(pending_loan.first().state, LOAN_STATE_PENDING)

        # Test case where loan with PENDING state does not exist
        approved_loan = Loan.objects.get_pending_loan_by_id(self.loan2.id)
        self.assertEqual(approved_loan.count(), 0)

    def test_get_pending_repayments_by_loan(self):
        # Test case where pending repayments exist for a loan
        pending_repayments = LoanRepayment.objects.get_pending_repayments_by_loan(self.loan1)
        self.assertEqual(pending_repayments.count(), 2)
        self.assertEqual(pending_repayments.filter(state=LOAN_STATE_PENDING).count(), 2)

        # Test case where no pending repayments exist for a loan
        pending_repayments2 = LoanRepayment.objects.get_pending_repayments_by_loan(self.loan2)
        self.assertEqual(pending_repayments2.count(), 0)
