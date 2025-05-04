from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class LanguagePreferenceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = None

        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile
                language = profile.preferred_language
            except UserProfile.DoesNotExist:
                pass  # Aucun profil associé

        if language:
            translation.activate(language)
        else:
            translation.deactivate_all()

        request.LANGUAGE_CODE = translation.get_language()
