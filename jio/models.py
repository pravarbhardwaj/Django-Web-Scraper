from django.db import models

class Jio(models.Model):
    monthly_rental = models.CharField(primary_key=True, max_length=264, unique=True)
    pack_validity = models.CharField(max_length=264)
    total_data = models.CharField(max_length=264)
    family_plan = models.CharField(max_length=264)
    data_with_rollover = models.CharField(max_length=264)
    sms_per_day = models.CharField(max_length=264)
    voice_call = models.CharField(max_length=264)
    amazon_prime = models.CharField(max_length=264)
    netflix_mobile = models.CharField(max_length=264)
    jio_tv = models.CharField(max_length=264)
    jio_security = models.CharField(max_length=264)
    jio_cloud = models.CharField(max_length=264)

    def __str__(self) -> str:
        return self.monthly_rental