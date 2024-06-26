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
   1. Register User API - It has two types of users Admin/Customer. Create both the users using postman
   2. Login API - You can use the same credentials used in the above API to login. This will create a jwt auth token and will set it in the cookies, and this cookie will be set for the other apis to use. So if admin is login last then all the API's will use admin cookie to perform action else otherwise.
   3. View Profile API - This will give you the details of last logged in user, as it uses the same jwt set above.
   4. Create Loan API - This will need amount and term and will create the loan for the logged in user, which will be in the pending state. This will also create the repayment entries.
   5. Approve Loan API - This will only be allowed to call after the admin login and will require the loanId. Once called it will approve the loan for the user.
   6. View User Loan - This will be used to view all the user loans, that are created by him.
   7. Add Repayment - This will need a loan id and amount, and will then balance the amount to all the repayments.

