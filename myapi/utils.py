from rest_framework.response import Response

def response_wrapper(data=None, status=200, url=None):
    return Response({
        "status": status,
        "data": data,
        "url": url
    }, status=status)
