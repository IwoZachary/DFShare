# Generated by Django 3.1.5 on 2021-01-13 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20210113_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_date', models.DateTimeField(auto_now_add=True, verbose_name='action_date')),
                ('action', django_enumfield.db.fields.EnumField(enum=myapp.models.Action)),
                ('userS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]