# Generated by Django 2.1.7 on 2019-03-10 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_stripepaymentintent'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripepaymentintent',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.SubscriptionType'),
        ),
    ]
