from django.urls import path
from . import views

urlpatterns = [
    # ... suas outras URLs ...
    path('avaliar-video/', views.avaliar_video, name='avaliar_video'),
]