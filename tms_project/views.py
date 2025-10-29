from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home(request):
    """Redirect to dashboard if authenticated, otherwise to login."""
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    return redirect('login')