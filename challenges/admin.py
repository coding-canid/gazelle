from django.contrib import admin

from .models import Challenge, ChallengeAssignment


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "is_active", "created_at")
    list_filter = ("language", "is_active")
    search_fields = ("title",)


@admin.register(ChallengeAssignment)
class ChallengeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("candidate", "challenge", "is_correct", "assigned_at", "submitted_at")
    list_filter = ("is_correct", "challenge")
    readonly_fields = ("token", "assigned_at", "submitted_at")
