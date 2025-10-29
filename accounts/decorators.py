from django.shortcuts import redirect
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if getattr(request.user, f'is_{role}')():
                return view_func(request, *args, **kwargs)
            # optionally show a "forbidden" page
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped
    return decorator
