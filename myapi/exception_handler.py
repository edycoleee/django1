from rest_framework.views import exception_handler
from .utils import response_wrapper

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response_wrapper(data=response.data, status=response.status_code, url=context['request'].path)
    return response
