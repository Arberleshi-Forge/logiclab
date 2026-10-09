from django.contrib import admin

from .models import CircuitImage


@admin.register(CircuitImage)
class CircuitImageAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at")
    search_fields = ("title", "ai_explanation")
