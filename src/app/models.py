from __future__ import annotations

import hashlib
import hmac
import secrets
from os import path
from uuid import uuid4

from django.conf import settings
from django.db import models


class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    location = models.CharField(max_length=50, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="votes"
    )
    token = models.ForeignKey("Token", on_delete=models.CASCADE, related_name="vote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate} {self.created_at}"


class MagicLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.UUIDField(default=uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="magic_link"
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.created_at}"


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.CharField(max_length=254)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}"

    def verify(self, passphrase: str) -> bool:
        _passwd = f"{passphrase}{self.salt.hex()}"
        key = hashlib.pbkdf2_hmac("sha256", _passwd.encode("utf-8"), self.salt, 600000)

        return hmac.compare_digest(key, self.token)

    @classmethod
    def create(cls):
        words = []

        with open(
            path.join(settings.BASE_DIR, "library", "eff_large_wordlist.txt")
        ) as file:
            for line in file:
                line_split = line.split("\t")
                words.append(line_split[1].strip())

        token = "-".join(secrets.choice(words) for _ in range(5))

        cls.objects.create(token=token)

        return token
