from django.contrib import admin

from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_by",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "name",
        "created_by__username",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "organization",
        "user",
        "role",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "organization__name",
        "user__username",
    ]

    list_filter = [
        "role",
        "created_at",
    ]
