# Generated by Django 2.1.7 on 2019-03-13 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_profile_account_selected_signup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='subscription_type',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
