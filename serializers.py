from tokenize import PlainToken
from rest_framework import serializers
from airtel.models import Airtel

class AirtelSerializer(serializers.ModelSerializers):
    class Meta:
        model = Airtel
        fields = ['monthly_rental', 'data_with_rollover', 'sms_per_day', 'local_std_roaming', 'amazon_prime']
