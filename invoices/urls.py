from django.urls import path
from . import views

urlpatterns = [
    path('upload-multiple-zips/', views.upload_multiple_zips, name='upload_multiple_zips'),
    path('test-lang/', views.test_lang_view, name='test_lang'),
]
