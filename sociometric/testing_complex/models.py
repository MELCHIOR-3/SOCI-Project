from django.db import models
from django.core.validators import MaxValueValidator

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

import uuid

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, default="Школа, номер. Образец [ГБОУ Школа № 853] ", blank=False)
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class student(models.Model):
    student_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    name = models.CharField(max_length=128, blank=True)
    surname = models.CharField(max_length=128, blank=True)
    patronymic = models.CharField(max_length=128, blank=True)

    gender = models.CharField(max_length=3,default="М/Ж", blank=True)

    school = models.CharField(max_length=100, default="Школа, номер. Образец: ГБОУ Школа № 853", blank=False)

    class_number = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(11)])
    class_litera = models.CharField(max_length=1, blank=True)
    
    birth_year = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(3000)])

    student_status = models.CharField(max_length=100, default="Информация отсутствует.", blank=False)

    def __str__(self):
        return str(str(self.surname) + " " + str(self.name) + " " + str(self.patronymic) + " " + str(self.class_number) + "-" + str(self.class_litera))
    
class test(models.Model):
    test_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    date = models.DateField()

    school = models.CharField(max_length=100, default="", blank=False)

    students_class = models.CharField(max_length=100, default="", blank=False)
    students_litera = models.CharField(max_length=100, default="", blank=False)

    checked = models.BooleanField(default=False)

    question_1A = models.CharField(max_length=512, blank=True)
    question_1B = models.CharField(max_length=512, blank=True)
    question_2A = models.CharField(max_length=512, blank=True)
    question_2B = models.CharField(max_length=512, blank=True)
    question_3A = models.CharField(max_length=512, blank=True)
    question_3B = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return str(self.date)

class test_answer(models.Model):
    test_answer_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    test_id = models.CharField(max_length=100, blank=True)

    name = models.CharField(max_length=128, blank=True)
    surname = models.CharField(max_length=128, blank=True)
    patronymic = models.CharField(max_length=128, blank=True)

    gender = models.CharField(max_length=3,default="М/Ж", blank=True)

    date = models.DateField()

    student_id = models.CharField(max_length=100, blank=True)

    school = models.CharField(max_length=100, default="", blank=False)

    students_class = models.CharField(max_length=100, default="", blank=False)
    students_litera = models.CharField(max_length=100, default="", blank=False)

    checked = models.BooleanField(default=False)

    answer_1A1 = models.CharField(max_length=512, blank=True)
    answer_1A2 = models.CharField(max_length=512, blank=True)
    answer_1A3 = models.CharField(max_length=512, blank=True)
    answer_1B1 = models.CharField(max_length=512, blank=True)
    answer_1B2 = models.CharField(max_length=512, blank=True)
    answer_1B3 = models.CharField(max_length=512, blank=True)
    answer_2A1 = models.CharField(max_length=512, blank=True)
    answer_2A2 = models.CharField(max_length=512, blank=True)
    answer_2A3 = models.CharField(max_length=512, blank=True)
    answer_2B1 = models.CharField(max_length=512, blank=True)
    answer_2B2 = models.CharField(max_length=512, blank=True)
    answer_2B3 = models.CharField(max_length=512, blank=True)
    answer_3A1 = models.CharField(max_length=512, blank=True)
    answer_3A2 = models.CharField(max_length=512, blank=True)
    answer_3A3 = models.CharField(max_length=512, blank=True)
    answer_3B1 = models.CharField(max_length=512, blank=True)
    answer_3B2 = models.CharField(max_length=512, blank=True)
    answer_3B3 = models.CharField(max_length=512, blank=True)

    student_status = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return str(str(self.date) + ' ' + str(self.student_status))
