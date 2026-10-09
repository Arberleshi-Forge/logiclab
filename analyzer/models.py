from django.db import models


class BooleanExpression(models.Model):
    original_expression = models.TextField()
    normalized_expression = models.TextField(blank=True)
    simplified_expression = models.TextField(blank=True)
    variables = models.CharField(max_length=255, blank=True)
    expression_type = models.CharField(max_length=40, blank=True)
    gate_count = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Shprehje Booleane"
        verbose_name_plural = "Shprehje Booleane"

    def __str__(self):
        return self.original_expression
