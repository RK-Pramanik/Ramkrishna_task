from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(LoginRequiredMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not self.required_role:
            return super().dispatch(request, *args, **kwargs)
        if not getattr(request.user, f'is_{self.required_role}')():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
