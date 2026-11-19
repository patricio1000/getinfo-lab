from django.db import models


class Info(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    cell_phone = models.CharField(max_length=20)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "info"

    def __str__(self):
        return f"{self.name} ({self.email})"
