from django.contrib import admin

from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "position", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("first_name", "last_name", "email", "position")
