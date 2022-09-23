from django.db import models

class Airtel(models.Model):
    monthly_rental = models.CharField(primary_key=True, max_length=264, unique=True)
    data_with_rollover = models.CharField(max_length=264)
    sms_per_day = models.CharField(max_length=264)
    local_std_roaming = models.CharField(max_length=264)
    amazon_prime = models.CharField(max_length=264)

    def __str__(self) -> str:
        return self.monthly_rental