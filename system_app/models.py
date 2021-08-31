from django.db import models

# Create your models here.
class Charts(models.Model):
    log_date = models.DateTimeField()
    log_category = models.CharField(max_length=150)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'chart'
        ordering = ["log_date"]

    def __str__(self):
        return str(self.id)