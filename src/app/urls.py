from __future__ import annotations

from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    login_forward,
    login_page,
    root,
    verify_passphrase,
    vote,
    vote_candidate,
)

urlpatterns = [
    path("", root, name="app_root"),
    path("vote/", vote, name="app_vote"),
    path("login/", login_forward, name="app_login_forward"),
    path("login/<token>/", login_page, name="app_login"),
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="app_logout",
    ),
    path("verify_passphrase/", verify_passphrase, name="app_verify_passphrase"),
    path("vote_candidate/", vote_candidate, name="app_vote_candidate"),
]
