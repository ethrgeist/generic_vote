from __future__ import annotations

import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from .models import Candidate, MagicLink, Token, Vote


def root(request):
    return redirect(reverse("app_login_forward"))


@login_required
def vote(request):
    template = loader.get_template("vote.html")
    extra_context = {
        "site_title": "voting",
        "candidates": Candidate.objects.all(),
    }
    return HttpResponse(template.render(extra_context, request))


def login_forward(request):
    if request.user.is_authenticated:
        return redirect(reverse("app_vote"))
    template = loader.get_template("index.html")
    extra_context = {
        "site_title": "index",
    }
    return HttpResponse(template.render(extra_context, request))


def login_page(request, token):
    if request.user.is_authenticated:
        return redirect(reverse("app_vote"))
    try:
        user = authenticate(request, token=token)
        if not user:
            return HttpResponseForbidden("Invalid token")
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        MagicLink.objects.filter(token=token).update(is_used=True)
        return redirect(reverse("app_vote"))
    except exceptions.ValidationError:
        template = loader.get_template("error.html")
        extra_context = {
            "site_title": "error",
        }
        return HttpResponseForbidden(template.render(extra_context, request))


@login_required
def verify_passphrase(request):
    body = json.loads(request.body)

    if not body.get("passphrase"):
        return JsonResponse(
            {"msg": "Invalid passphrase", "status": "failed"}, status=400
        )

    try:
        token = Token.objects.get(token=body["passphrase"])
        if not token.is_active:
            return JsonResponse(
                {"msg": "Token already spend.", "status": "spend"}, status=200
            )
        request.session["token_valided"] = str(token.id)
        return JsonResponse({"msg": "Token valided", "status": "success"}, status=200)
    except Token.DoesNotExist:
        return JsonResponse(
            {"msg": "Invalid passphrase", "status": "failed"}, status=400
        )


@login_required
def vote_candidate(request):
    body = json.loads(request.body)

    if not request.session.get("token_valided"):
        return JsonResponse(
            {"msg": "Token not valided", "status": "failed"}, status=400
        )

    candidates = body["candidates"]

    try:
        for candidate in candidates:
            candidate = Candidate.objects.get(id=candidate)
            token = Token.objects.get(
                id=request.session["token_valided"], is_active=True
            )
            Vote.objects.create(candidate=candidate, token=token)
    except (Candidate.DoesNotExist, Token.DoesNotExist):
        return JsonResponse(
            {"msg": "Invalid candidate", "status": "failed"}, status=400
        )

    token.is_active = False
    token.save()

    request.session["token_valided"] = None

    return JsonResponse({"msg": "Vote success", "status": "success"}, status=200)
