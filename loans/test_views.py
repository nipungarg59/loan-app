import datetime
import decimal
from unittest import TestCase

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from loans.models import Loan, LoanRepayment
from loans.constants import LOAN_STATE_APPROVED, LOAN_STATE_PENDING, LOAN_STATE_PAID
from users.constants import USER_ROLE_CUSTOMER, USER_ROLE_ADMIN
from users.models import User


class CreateLoanAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()
        Loan.objects.all().delete()
        LoanRepayment.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create(
            user_name='customer',
            password=make_password('password'),
            role=USER_ROLE_CUSTOMER
        )
        setattr(self.user, "is_authenticated", True)
        self.client.force_authenticate(user=self.user)

    def test_create_loan_success(self):
        url = reverse('create-loan')
        data = {
            'amount': '10000.00',
            'term': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Loan created successfully')
        self.assertEqual(Loan.objects.filter(user=self.user).count(), 1)

    def test_create_loan_invalid_data(self):
        url = reverse('create-loan')
        data = {
            'amount': '',
            'term': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApproveLoanAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()
        Loan.objects.all().delete()
        LoanRepayment.objects.all().delete()

        self.client = APIClient()
        self.admin_user = User.objects.create(
            user_name='admin',
            password=make_password('password'),
            role=USER_ROLE_ADMIN
        )
        setattr(self.admin_user, "is_authenticated", True)
        self.client.force_authenticate(user=self.admin_user)

        self.customer_user = User.objects.create(
            user_name='customer',
            password=make_password('password'),
            role=USER_ROLE_CUSTOMER
        )
        self.loan = Loan.objects.create(
            user=self.customer_user,
            amount=decimal.Decimal('10000.00'),
            term=3,
            state=LOAN_STATE_PENDING
        )

    def test_approve_loan_success(self):
        url = reverse('approve-loan', args=[self.loan.id])
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Loan approved successfully')
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.state, 'Approved')

    def test_approve_loan_invalid_loan(self):
        url = reverse('approve-loan', args=[999])
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Either loan is not in pending state or loan is already approved')


class ListUserLoansAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()
        Loan.objects.all().delete()
        LoanRepayment.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create(
            user_name='customer',
            password=make_password('password'),
            role=USER_ROLE_CUSTOMER
        )
        setattr(self.user, "is_authenticated", True)
        self.client.force_authenticate(user=self.user)
        self.loan = Loan.objects.create(
            user=self.user,
            amount=decimal.Decimal('10000.00'),
            term=3,
            state=LOAN_STATE_PENDING
        )

    def test_list_user_loans_success(self):
        url = reverse('my-loans')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User loans fetched successfully')
        self.assertEqual(len(response.data['data']), 1)

    def test_list_user_loans_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('my-loans')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AddRepaymentAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()
        Loan.objects.all().delete()
        LoanRepayment.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create(
            user_name='customer',
            password=make_password('password'),
            role='Customer'
        )
        setattr(self.user, "is_authenticated", True)
        self.client.force_authenticate(user=self.user)
        self.loan = Loan.objects.create(
            user=self.user,
            amount=decimal.Decimal('10000.00'),
            term=3,
            state=LOAN_STATE_APPROVED
        )
        self.repayment1 = LoanRepayment.objects.create(
            loan=self.loan,
            amount=decimal.Decimal('3333.33'),
            amount_paid=decimal.Decimal('0.00'),
            repayment_date=datetime.datetime.now()
        )
        self.repayment2 = LoanRepayment.objects.create(
            loan=self.loan,
            amount=decimal.Decimal('3333.33'),
            amount_paid=decimal.Decimal('0.00'),
            repayment_date=datetime.datetime.now() + datetime.timedelta(weeks=1)
        )
        self.repayment3 = LoanRepayment.objects.create(
            loan=self.loan,
            amount=decimal.Decimal('3333.34'),
            amount_paid=decimal.Decimal('0.00'),
            repayment_date=datetime.datetime.now() + datetime.timedelta(weeks=2)
        )

    def test_add_repayment_success(self):
        url = reverse('add-repayment', args=[self.loan.id])
        data = {
            'amount': '3333.33'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Repayment added successfully')
        self.repayment1.refresh_from_db()
        self.assertEqual(self.repayment1.amount_paid, decimal.Decimal('3333.33'))

    def test_add_repayment_invalid_loan(self):
        url = reverse('add-repayment', args=[999])
        data = {
            'amount': '3333.33'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Either loan is not approved or does not exist')

    def test_add_repayment_partial(self):
        url = reverse('add-repayment', args=[self.loan.id])
        data = {
            'amount': '5000.00'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Repayment added successfully')
        self.repayment1.refresh_from_db()
        self.repayment2.refresh_from_db()
        self.assertEqual(self.repayment1.amount_paid, decimal.Decimal('3333.33'))
        self.assertEqual(self.repayment2.amount_paid, decimal.Decimal('1666.67'))

