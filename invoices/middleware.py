from django.utils import translation
from .models import UserProfile


class LanguagePreferenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_profile = request.user.userprofile
                language = user_profile.preferred_language
                translation.activate(language)
                request.LANGUAGE_CODE = language
            except UserProfile.DoesNotExist:
                pass  # Pas encore de profil, rien à faire

        response = self.get_response(request)
        return response
