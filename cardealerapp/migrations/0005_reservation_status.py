# Generated by Django 4.2.3 on 2024-03-27 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardealerapp', '0004_servicebooking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Expired', 'Expired'), ('Valid', 'Valid')], default='Valid', max_length=20),
        ),
    ]
