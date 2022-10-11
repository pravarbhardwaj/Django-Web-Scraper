from rest_framework import serializers
from jio.models import Jio

class JioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Jio
        fields = ['monthly_rental', 'voice_call', 'pack_validity', 'total_data', 'family_plan', 'data_with_rollover', 'sms_per_day', 'amazon_prime',
        'netflix_mobile', 'jio_tv', 'jio_cloud', 'jio_security']
