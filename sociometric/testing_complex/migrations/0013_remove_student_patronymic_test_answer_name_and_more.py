# Generated by Django 5.1.5 on 2025-02-19 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_complex', '0012_student_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='patronymic',
        ),
        migrations.AddField(
            model_name='test_answer',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='test_answer',
            name='patronymic',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='test_answer',
            name='surname',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
