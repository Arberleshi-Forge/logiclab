from django.db import models


class CircuitImage(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="circuit_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ai_explanation = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Imazh qarku"
        verbose_name_plural = "Imazhe qarqesh"

    def __str__(self):
        return self.title
