from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 🆕 User registration page
    path('signup/', views.signup_view, name='signup'),

    # 🏠 Optional: profile/dashboard (if you want one)
    path('profile/', views.profile_view, name='profile'),
]
