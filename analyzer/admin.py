from django.contrib import admin

from .models import BooleanExpression


@admin.register(BooleanExpression)
class BooleanExpressionAdmin(admin.ModelAdmin):
    list_display = ("original_expression", "simplified_expression", "expression_type", "created_at")
    search_fields = ("original_expression", "simplified_expression", "variables")
    list_filter = ("expression_type", "created_at")
