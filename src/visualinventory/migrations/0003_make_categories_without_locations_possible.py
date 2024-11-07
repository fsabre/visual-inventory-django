# Generated by Django 5.0.3 on 2024-11-07 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualinventory', '0002_create_initial_space'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='locations',
            field=models.ManyToManyField(blank=True, related_name='stored_categories', to='visualinventory.location'),
        ),
    ]
