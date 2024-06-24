from rest_framework.response import Response


def success_response(data, status_code=200, message='Success'):
    return Response({
        'status': 'success',
        'message': message,
        'data': data
    }, status=status_code)


def error_response(error, status_code=400, message='Something Went Wrong'):
    return Response({
        'status': 'error',
        'message': message,
        'error': error
    }, status=status_code)
