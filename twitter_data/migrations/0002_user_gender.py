# Generated by Django 4.2.6 on 2023-10-30 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'man'), ('F', 'woman'), ('X', 'nonbinary')], default='M', max_length=1),
        ),
    ]
