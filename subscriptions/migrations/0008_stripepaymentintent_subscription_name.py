# Generated by Django 2.1.7 on 2019-03-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripepaymentintent',
            name='subscription_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
