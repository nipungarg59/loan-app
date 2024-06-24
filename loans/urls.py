from django.urls import path
from loans.views import CreateLoanAPIView, ApproveLoanAPIView, ListUserLoansAPIView, AddRepaymentAPIView

urlpatterns = [
    path('create/', CreateLoanAPIView.as_view(), name='create-loan'),
    path('approve/<int:loan_id>/', ApproveLoanAPIView.as_view(), name='approve-loan'),
    path('my-loans/', ListUserLoansAPIView.as_view(), name='my-loans'),
    path('add-repayment/<int:repayment_id>/', AddRepaymentAPIView.as_view(), name='add-repayment'),
]
