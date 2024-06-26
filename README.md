# Setup 
1. Clone the repo
2. cd into the project directory

### Setup using script
* `sh setup.sh`

If the above script fails then make sure latest version of python is installed
and again retry.

# Running the Project
* `sh run.sh`

This will start the project on port 8000

# Usage -
1. Import the postman collection - https://api.postman.com/collections/1937110-8b117cde-aecb-4e5f-b257-27d6b4015592?access_key=PMAT-01J1AV61KN7F8W5CP1ZSJZGG0A
2. Use API in the following order -
   1. **Register User API** - /user/register/
      1. It has two types of users Admin/Customer. 
      2. Create both the users using postman
   2. **Login API** - /user/login/
      1. You can use the same credentials used in the above API to login. 
      2. This will create a jwt auth token and will set it in the cookies, and this cookie will be set for the other apis to use. 
      3. So if admin is login last then all the API's will use admin cookie to perform action else otherwise.
   3. **View Profile API** - /user/my-profile/
      1. This will give you the details of last logged in user, as it uses the same jwt set above.
   4. **Create Loan API** - /loan/create/
      1. This will need amount and term and will create the loan for the logged in user, which will be in the pending state. 
      2. This will also create the repayment entries.
   5. **Approve Loan API** - /loan/approve/<loan_id>/ 
      1. This will only be allowed to call after the admin login and will require the loanId. 
      2. Once called it will approve the loan for the user.
   6. **View User Loan** - /loan/my-loans/
      1. This will be used to view all the user loans, that are created by him.
   7. **Add Repayment** - /loan/add-repayment/1/
      1. This will need a loan id and amount, and will then balance the amount to all the repayments.

# DB
1. It uses sqlite db which is file based. Reason is to make it easy to setup.

# Framework
1. Uses Django (MVC Framework) to create models, views
2. Uses Django-Rest-Framework to make views more robust.
