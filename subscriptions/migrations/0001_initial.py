# Generated by Django 2.1.7 on 2019-03-08 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('max_websites', models.IntegerField(default=0)),
                ('max_visits', models.IntegerField(default=0)),
                ('can_geolocation', models.BooleanField(default=False)),
                ('yearly_price', models.IntegerField(default=0, help_text='Yearly price in dollars')),
                ('monthly_price', models.IntegerField(default=0, help_text='Monthly price in dollars')),
            ],
        ),
    ]