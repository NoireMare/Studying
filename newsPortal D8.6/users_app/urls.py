from django.urls import path
from .views import change_group_to_authors, ProfileView, change_group_to_common

urlpatterns = [
    path('', ProfileView.as_view()),
    path('upgrade_to_authors/', change_group_to_authors),
    path('upgrade_to_common/', change_group_to_common),
]
