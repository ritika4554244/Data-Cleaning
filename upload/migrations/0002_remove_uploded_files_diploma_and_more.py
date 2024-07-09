# Generated by Django 4.1.6 on 2023-03-20 11:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("upload", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="uploded_files", name="diploma",),
        migrations.AddField(
            model_name="uploded_files",
            name="file_title",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uploded_files",
            name="validation_and_cleaning_files",
            field=models.FileField(
                default=None, max_length=250, null=True, upload_to="JSON_FILES/"
            ),
        ),
    ]
