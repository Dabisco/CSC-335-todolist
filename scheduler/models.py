from django.db import models
from account.models import User

class ScheduledEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduled_events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_datetime = models.CharField(max_length=255) 
    end_datetime = models.CharField(max_length=255, blank=True, null=True) 
    location = models.CharField(max_length=255, blank=True, null=True)
    reminder = models.BooleanField(default=False)
    is_all_day = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_datetime']
        verbose_name_plural = "Scheduled Events"

    def __str__(self):
        return f"{self.title} - {self.start_datetime}"

    
    
