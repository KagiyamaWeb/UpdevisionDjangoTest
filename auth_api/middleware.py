from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class AutoRefreshJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path in ['/api/signin/', '/api/signup/']:
            return response

        try:
            auth = JWTAuthentication().authenticate(request)
            if auth and auth[0].is_authenticated:
                new_token = RefreshToken.for_user(auth[0]).access_token
                response['X-New-Access-Token'] = str(new_token)
        except (InvalidToken, AuthenticationFailed):
            pass
            
        return response
