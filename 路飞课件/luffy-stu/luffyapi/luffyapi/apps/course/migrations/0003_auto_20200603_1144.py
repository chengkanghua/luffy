# Generated by Django 2.2.5 on 2020-06-03 11:44

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20200602_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_video',
            field=models.FileField(blank=True, null=True, upload_to='video', verbose_name='封面视频'),
        ),
        migrations.AlterField(
            model_name='course',
            name='brief',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=2048, null=True, verbose_name='详情介绍'),
        ),
    ]
