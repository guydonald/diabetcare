from django.http import HttpResponseForbidden

class SessionSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            
            # Vérifications en 3 couches
            token_valid = str(user.security_token) == request.session.get('security_token')
            ip_valid = user.last_login_ip == request.META.get('REMOTE_ADDR')
            session_valid = user.current_session_id == request.session.session_key

            if not (token_valid and ip_valid and session_valid):
                user.rotate_security_token()
                request.session.flush()
                return HttpResponseForbidden("Activité suspecte détectée - Veuillez vous reconnecter")

        return self.get_response(request)