from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'user_role'):
                if request.user.user_role.role == role:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
        return _wrapped_view
    return decorator
