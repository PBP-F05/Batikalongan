from django.shortcuts import redirect
from functools import wraps 

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('is_admin'):
            return view_func(request, *args, **kwargs)
        return redirect('main:main_landing_page')  # Replace with your desired redirect
    return _wrapped_view
