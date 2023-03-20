from __future__ import annotations

from django.contrib import admin

from .models import Candidate, MagicLink, Token, Vote


class CandidateAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("_name", "vote_count", "location", "created_at", "updated_at")

    def _name(self, obj):
        return obj

    def vote_count(self, obj):
        return obj.votes.count()


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ("candidate", "token", "created_at", "updated_at")

    list_display = ("candidate", "token", "created_at", "updated_at")

    def has_delete_permission(self, _request, _obj=None):
        return True

    def has_change_permission(self, _request, _obj=None):
        return False

    def has_add_permission(self, _request):
        return False


class TokenAdmin(admin.ModelAdmin):
    list_display = ("id", "_token", "is_active")
    readonly_fields = ("id", "_token", "is_active")

    def _token(self, obj):
        _token = obj.token
        length = len(_token)
        to_replace = length - 10
        _token = _token[:5] + "*" * to_replace + _token[-5:]
        return _token

    def has_delete_permission(self, _request, _obj=None):
        return True

    def has_change_permission(self, _request, _obj=None):
        return False

    def has_add_permission(self, _request):
        return False


class MagicLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token", "is_used", "created_at", "updated_at")
    readonly_fields = ("id", "user", "token", "is_used", "created_at", "updated_at")

    def has_delete_permission(self, _request, _obj=None):
        return True

    def has_change_permission(self, _request, _obj=None):
        return False

    def has_add_permission(self, _request):
        return False


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(MagicLink, MagicLinkAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Vote, VoteAdmin)
