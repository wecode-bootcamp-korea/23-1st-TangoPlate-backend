import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings            import SECRET_KEY
from .models                import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token           = request.headers.get("authorization", None)
            if not token:
                request.user = None
            else:
                user            = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                request.user    = User.objects.get(id = user['id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)

    return wrapper
