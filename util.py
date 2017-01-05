from functools import wraps
from flask import current_app
from flask_login import current_user

from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect


def require_username(username, fallback_view):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if current_user.username != username:
                return redirect(url_for(fallback_view))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
