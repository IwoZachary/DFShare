# Generated by Django 3.1.5 on 2021-01-16 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20210116_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedfile',
            name='id',
        ),
        migrations.AlterField(
            model_name='sharedfile',
            name='fileS',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.filemod'),
        ),
    ]