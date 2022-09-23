# Generated by Django 4.1.1 on 2022-09-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airtel',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('monthly_rental', models.CharField(max_length=264, unique=True)),
                ('data_with_rollover', models.CharField(max_length=264)),
                ('sms_per_day', models.CharField(max_length=264)),
                ('local_std_roaming', models.CharField(max_length=264)),
                ('amazon_prime', models.CharField(max_length=264)),
            ],
        ),
    ]
