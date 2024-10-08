# Generated by Django 4.2.13 on 2024-07-27 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='card_last4',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='cardholder_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='cardholder_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
