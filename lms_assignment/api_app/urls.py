from django.urls import path
from .views import lmsItemViews

urlpatterns = [
        path('lms-items/', lmsItemViews.as_view()),
        path('lms-items/<int:id>', lmsItemViews.as_view(), name = 'lms'),
]
