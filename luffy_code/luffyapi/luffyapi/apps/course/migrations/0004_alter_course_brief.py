# Generated by Django 3.2.25 on 2024-05-18 11:47

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20240518_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='brief',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=2048, null=True, verbose_name='课程概述'),
        ),
    ]