from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from generics.responses.responses import success_response, error_response
from users.authentication.jwt_utils import generate_jwt_token
from users.models import User
from users.serializers import UserSerializer


class RegisterUserAPIView(APIView):
    """
    This API will be used to register yourself as a new user
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=status.HTTP_201_CREATED, message="User Created Successfully")
        return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class FetchUserDetailsAPIView(APIView):
    """
    This API is to get the details of current user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return success_response(serializer.data)


class LoginAPIView(APIView):
    """
    This API will first check the credentials,
    if this validation works then it will generate the jwt and set in cookies with name jwt
    """
    def post(self, request):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        user = User.objects.authenticate(user_name, password)
        if user is not None:
            token = generate_jwt_token(user)
            data = {
                'token': token
            }
            response = success_response(data, status.HTTP_200_OK, 'Login successful')
            response.set_cookie('jwt', token, httponly=True, samesite='Lax')
            return response
        return error_response({}, status.HTTP_401_UNAUTHORIZED, 'Invalid Credentials')
