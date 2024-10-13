# Generated by Django 5.0.6 on 2024-10-04 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Datashop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datesend', models.DateField()),
                ('num_order', models.CharField(max_length=20)),
                ('order', models.TextField()),
                ('product', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('totalPrece', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField()),
                ('message', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
