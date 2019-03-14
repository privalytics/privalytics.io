# Generated by Django 2.1.7 on 2019-03-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190313_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account_selected_signup',
            field=models.CharField(help_text='The account type selected while signing up', max_length=50, null=True),
        ),
    ]