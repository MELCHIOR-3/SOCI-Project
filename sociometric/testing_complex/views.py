from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from .models import *

import json

from urllib.parse import urlparse, parse_qs

from datetime import datetime as dt
import datetime

#import mysql.connector

#conn = mysql.connector.connect(
#    host="89.111.141.89",
#    port="3306",
#    user='dev_user',
#    password='Dev_user13',
#    database='dev_soci',
#    )

sociyounger_questions={"first_question_A":"Ваш класс отправляется в поход. Кого бы ты хотел видеть капитаном вашего класса?",
             "first_question_B":"Кого бы ты не выбрал капитаном?",
             "second_question_A":"У тебя день рождения. Кого из одноклассников ты хотел бы пригласить на свой день рождения?",
             "second_question_B":"Кого из одноклассников ты не пригласишь на свой день рождения?",
             "third_question_A":"Ты переходишь в другой класс. С кем бы ты хотел продолжить совместно учиться в новом коллективе?",
             "third_question_B":"С кем бы ты не хотел продолжить учиться в новом коллективе?"
             }
sociolder_questions={"first_question_A":"Ваш класс участвует в КВН. Кого бы ты хотел видеть капитаном команды?",
             "first_question_B":"Кого бы ты не выбрал капитаном команды?",
             "second_question_A":"Тебя пригласили на вечеринку вместе с твоими друзьями. Кого из одноклассников ты хотел бы пригласить с собой?",
             "second_question_B":"Кого из одноклассников ты хотел бы пригласить с собой?",
             "third_question_A":"Ты переходишь в другой класс. С кем бы ты хотел продолжить совместно учиться в новом коллективе?",
             "third_question_B":"С кем бы ты не хотел продолжить учиться в новом коллективе?"
             }

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")    
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        pass
    return render(request, 'account/login.html') 

def log_out(request):
    logout(request=request)
    return HttpResponse('Выход осуществлен!')

@login_required(login_url='/')
def home(request):
    school = request.user.profile.school
    clasess_info = student.objects.filter(school=school)
    list_classes = []
    for cls in clasess_info:
        list_classes.append(f"{cls.class_number}-{cls.class_litera}")
    list_classes = list(set(list_classes))

    context = {
        "school":school,
        "classes":list_classes
        }
    return render(request, 'main/index.html', context=context) 

@login_required(login_url='/')
def add_student(request):
    school = request.user.profile.school
    context = {
        "school":school,
        }
    if request.method == 'POST':
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        patronymic = request.POST.get("patronymic")
        class_number = int(request.POST.get("class_number"))
        class_litera = (request.POST.get("class_litera")).upper()
        birth_year = int(request.POST.get("birth_year"))
        gender = request.POST.get("gender")
        created_student = student(name=name, surname=surname, patronymic=patronymic, gender=gender.lower(), class_number=class_number, class_litera=class_litera, birth_year=birth_year, school=school)
        created_student.save()
    return render(request, 'main/add_student.html', context=context)

@login_required(login_url='/')
def class_info(request, data):
    school = request.user.profile.school
    class_number = int(data.split('-')[0])
    class_litera = data.split('-')[1]
    test_request = ''
    matrix_students_dict={}
    
    r1 = student.objects.filter(school=school, class_number=class_number, class_litera=class_litera)
    students_dict = dict()
    for i in r1:
        students_dict[f'{i.surname} {i.name} {i.patronymic} ({i.student_status})'] = i.student_id
    yesterday = dt.now() - datetime.timedelta(days=1)
    formatted_yesterday = yesterday.strftime('%Y-%m-%d')
    entry = test_answer.objects.filter(school=school, students_class=class_number, students_litera=class_litera, checked = False, date__range=["2011-01-01", formatted_yesterday])
    if entry.exists():
        # Создание матрицы М
        count_students = len(entry)
        matrix = []
        a = ["0"]
        for i in entry:
            a.append(f'{i.surname} {i.name}')
        matrix.append(a)
        for i in entry:
            matrix.append([f'{i.surname} {i.name}']+([0]*len(entry)))
        number_of_elections = 0
        # Заполнение информацией матрицы М. На случай если какой-то испытуемый сможт ввести некоректные данные, эти данные исключаются(try except)
        for i in entry:
            matrix_student = matrix[0].index(f'{i.surname} {i.name}')
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1A1)] = matrix[matrix_student][matrix[0].index(i.answer_1A1)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1A2)] = matrix[matrix_student][matrix[0].index(i.answer_1A2)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1A3)] = matrix[matrix_student][matrix[0].index(i.answer_1A3)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1B1)] = matrix[matrix_student][matrix[0].index(i.answer_1B1)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1B2)] = matrix[matrix_student][matrix[0].index(i.answer_1B2)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_1B3)] = matrix[matrix_student][matrix[0].index(i.answer_1B3)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2A1)] = matrix[matrix_student][matrix[0].index(i.answer_2A1)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2A2)] = matrix[matrix_student][matrix[0].index(i.answer_2A2)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2A3)] = matrix[matrix_student][matrix[0].index(i.answer_2A3)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2B1)] = matrix[matrix_student][matrix[0].index(i.answer_2B1)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2B2)] = matrix[matrix_student][matrix[0].index(i.answer_2B2)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_2B3)] = matrix[matrix_student][matrix[0].index(i.answer_2B3)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3A1)] = matrix[matrix_student][matrix[0].index(i.answer_3A1)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3A2)] = matrix[matrix_student][matrix[0].index(i.answer_3A2)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3A3)] = matrix[matrix_student][matrix[0].index(i.answer_3A3)] + 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3B1)] = matrix[matrix_student][matrix[0].index(i.answer_3B1)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3B2)] = matrix[matrix_student][matrix[0].index(i.answer_3B2)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass
            try:
                matrix[matrix_student][matrix[0].index(i.answer_3B3)] = matrix[matrix_student][matrix[0].index(i.answer_3B3)] - 1
                number_of_elections = number_of_elections + 1
            except:
                pass

            K = number_of_elections/count_students
            matrix_count = -1
            for i in matrix[0]:
                count_choices = []
                matrix_count = matrix_count + 1
                if i == "0":
                    pass
                else:
                    for n in matrix:
                        if isinstance(n[matrix_count], int):
                            count_choices.append(n[matrix_count])
                matrix_students_dict[i]=sum(count_choices)
            del matrix_students_dict["0"]
            for i in matrix_students_dict:
                if 2*(matrix_students_dict[i]/(count_students - 1)) >= K:
                    matrix_students_dict[i] = "Звезда"
                elif 1.5*(matrix_students_dict[i]/(count_students - 1)) >= K:
                    matrix_students_dict[i] = "Предпочитаемый(-ая)"
                elif (matrix_students_dict[i]/(count_students - 1)) < K*1.5 and (matrix_students_dict[i]/(count_students - 1)) > K/1.5:
                    matrix_students_dict[i] = "Принятый(-ая)"
                elif (matrix_students_dict[i]/(count_students - 1)) < K/1.5 and (matrix_students_dict[i]/(count_students - 1)) > K/2:
                    matrix_students_dict[i] = "Непринятый(-ая)"
                else:
                    matrix_students_dict[i] = "Отвергнутый(-ая)"
            for i in entry:
                i.checked = True
                i.save()

    for i in matrix_students_dict:
        student_update = student.objects.get(surname=i.split(' ')[0], name=i.split(' ')[1], school=school, class_litera=class_litera, class_number=class_number)
        student_update.student_status = matrix_students_dict[i]
        student_update.save()
    context = {
        "school":school,
        "class_name":data,
        "students":students_dict,
        "test_request":test_request
        }
    return render(request, 'main/class.html', context=context)

@login_required(login_url='/')
def class_soci_info(request, data):
    return HttpResponse("Тест завершен!")

@login_required(login_url='/')
def student_info(request, data):
    school = request.user.profile.school
    student_1 = student.objects.filter(student_id = data)[0]
    test_answer_student = test_answer.objects.filter(student_id=data, checked=True).order_by('date')[0]
    test_student = test.objects.get(test_id=test_answer_student.test_id)
    answer_1A1_student = student.objects.get(school=school, surname=(test_answer_student.answer_1A1).split(" ")[0], name=(test_answer_student.answer_1A1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1A1_student_id = answer_1A1_student.student_id
    answer_1A1_student_status = answer_1A1_student.student_status
    answer_1A2_student = student.objects.get(school=school, surname=(test_answer_student.answer_1A2).split(" ")[0], name=(test_answer_student.answer_1A2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1A2_student_id = answer_1A2_student.student_id
    answer_1A2_student_status = answer_1A2_student.student_status
    answer_1A3_student = student.objects.get(school=school, surname=(test_answer_student.answer_1A3).split(" ")[0], name=(test_answer_student.answer_1A3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1A3_student_id = answer_1A3_student.student_id
    answer_1A3_student_status = answer_1A3_student.student_status
    answer_1B1_student = student.objects.get(school=school, surname=(test_answer_student.answer_1B1).split(" ")[0], name=(test_answer_student.answer_1B1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1B1_student_id = answer_1B1_student.student_id
    answer_1B1_student_status = answer_1B1_student.student_status
    answer_1B2_student = student.objects.get(school=school, surname=(test_answer_student.answer_1B2).split(" ")[0], name=(test_answer_student.answer_1B2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1B2_student_id = answer_1B2_student.student_id
    answer_1B2_student_status = answer_1B2_student.student_status
    answer_1B3_student = student.objects.get(school=school, surname=(test_answer_student.answer_1B3).split(" ")[0], name=(test_answer_student.answer_1B3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_1B3_student_id = answer_1B3_student.student_id
    answer_1B3_student_status = answer_1B3_student.student_status
    answer_2A1_student = student.objects.get(school=school, surname=(test_answer_student.answer_2A1).split(" ")[0], name=(test_answer_student.answer_2A1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2A1_student_id = answer_2A1_student.student_id
    answer_2A1_student_status = answer_2A1_student.student_status
    answer_2A2_student = student.objects.get(school=school, surname=(test_answer_student.answer_2A2).split(" ")[0], name=(test_answer_student.answer_2A2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2A2_student_id = answer_2A2_student.student_id
    answer_2A2_student_status = answer_2A2_student.student_status
    answer_2A3_student = student.objects.get(school=school, surname=(test_answer_student.answer_2A3).split(" ")[0], name=(test_answer_student.answer_2A3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2A3_student_id = answer_2A3_student.student_id
    answer_2A3_student_status = answer_2A3_student.student_status
    answer_2B1_student = student.objects.get(school=school, surname=(test_answer_student.answer_2B1).split(" ")[0], name=(test_answer_student.answer_2B1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2B1_student_id = answer_2B1_student.student_id
    answer_2B1_student_status = answer_2B1_student.student_status
    answer_2B2_student = student.objects.get(school=school, surname=(test_answer_student.answer_2B2).split(" ")[0], name=(test_answer_student.answer_2B2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2B2_student_id = answer_2B2_student.student_id
    answer_2B2_student_status = answer_2B2_student.student_status
    answer_2B3_student = student.objects.get(school=school, surname=(test_answer_student.answer_2B3).split(" ")[0], name=(test_answer_student.answer_2B3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_2B3_student_id = answer_2B3_student.student_id
    answer_2B3_student_status = answer_2B3_student.student_status
    answer_3A1_student = student.objects.get(school=school, surname=(test_answer_student.answer_3A1).split(" ")[0], name=(test_answer_student.answer_3A1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3A1_student_id = answer_3A1_student.student_id
    answer_3A1_student_status = answer_3A1_student.student_status
    answer_3A2_student = student.objects.get(school=school, surname=(test_answer_student.answer_3A2).split(" ")[0], name=(test_answer_student.answer_3A2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3A2_student_id = answer_3A2_student.student_id
    answer_3A2_student_status = answer_3A2_student.student_status
    answer_3A3_student = student.objects.get(school=school, surname=(test_answer_student.answer_3A3).split(" ")[0], name=(test_answer_student.answer_3A3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3A3_student_id = answer_3A3_student.student_id
    answer_3A3_student_status = answer_3A3_student.student_status
    answer_3B1_student = student.objects.get(school=school, surname=(test_answer_student.answer_3B1).split(" ")[0], name=(test_answer_student.answer_3B1).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3B1_student_id = answer_3B1_student.student_id
    answer_3B1_student_status = answer_3B1_student.student_status
    answer_3B2_student = student.objects.get(school=school, surname=(test_answer_student.answer_3B2).split(" ")[0], name=(test_answer_student.answer_3B2).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3B2_student_id = answer_3B2_student.student_id
    answer_3B2_student_status = answer_3B2_student.student_status
    answer_3B3_student = student.objects.get(school=school, surname=(test_answer_student.answer_3B3).split(" ")[0], name=(test_answer_student.answer_3B3).split(" ")[1], class_number = student_1.class_number, class_litera = student_1.class_litera)
    answer_3B3_student_id = answer_3B3_student.student_id
    answer_3B3_student_status = answer_3B3_student.student_status


    context = {
        "school":school,
        "surname":student_1.surname,
        "name":student_1.name,
        "patronymic":student_1.patronymic,
        "student_status":student_1.student_status,
        "student_class": f"{student_1.class_number}-{student_1.class_litera}",
        "first_question_A":test_student.question_1A,
        "answer_1A1": test_answer_student.answer_1A1,
        "answer_1A1_student_id":answer_1A1_student_id,
        "answer_1A1_student_status":answer_1A1_student_status,
        "answer_1A2": test_answer_student.answer_1A2,
        "answer_1A2_student_id":answer_1A2_student_id,
        "answer_1A2_student_status":answer_1A2_student_status,
        "answer_1A3": test_answer_student.answer_1A3,
        "answer_1A3_student_id":answer_1A3_student_id,
        "answer_1A3_student_status":answer_1A3_student_status,
        "first_question_B":test_student.question_1B,
        "answer_1B1":test_answer_student.answer_1B1,
        "answer_1B1_student_id":answer_1B1_student_id,
        "answer_1B1_student_status":answer_1B1_student_status,
        "answer_1B2":test_answer_student.answer_1B2,
        "answer_1B2_student_id":answer_1B2_student_id,
        "answer_1B2_student_status":answer_1B2_student_status,
        "answer_1B3":test_answer_student.answer_1B3,
        "answer_1B3_student_id":answer_1B3_student_id,
        "answer_1B3_student_status": answer_1B3_student_status,
        "second_question_A":test_student.question_2A,
        "answer_2A1": test_answer_student.answer_2A1,
        "answer_2A1_student_id":answer_2A1_student_id,
        "answer_2A1_student_status":answer_2A1_student_status,
        "answer_2A2":test_answer_student.answer_2A2,
        "answer_2A2_student_id":answer_2A2_student_id,
        "answer_2A2_student_status":answer_2A2_student_status,
        "answer_2A3":test_answer_student.answer_2A3,
        "answer_2A3_student_id":answer_2A3_student_id,
        "answer_2A3_student_status":answer_2A3_student_status,
        "second_question_B":test_student.question_2B,
        "answer_2B1":test_answer_student.answer_2B1,
        "answer_2B1_student_id":answer_2B1_student_id,
        "answer_2B1_student_status":answer_2B1_student_status,
        "answer_2B2":test_answer_student.answer_2B2,
        "answer_2B2_student_id":answer_2B2_student_id,
        "answer_2B2_student_status":answer_2B2_student_status,
        "answer_2B3":test_answer_student.answer_2B3,
        "answer_2B3_student_id":answer_2B3_student_id,
        "answer_2B3_student_status":answer_2B3_student_status,
        "third_question_A":test_student.question_3A,
        "answer_3A1":test_answer_student.answer_3A1,
        "answer_3A1_student_id":answer_3A1_student_id,
        "answer_3A1_student_status":answer_3A1_student_status,
        "answer_3A2": test_answer_student.answer_3A2,
        "answer_3A2_student_id":answer_3A2_student_id,
        "answer_3A2_student_status":answer_3A2_student_status,
        "answer_3A3":test_answer_student.answer_3A3,
        "answer_3A3_student_id":answer_3A3_student_id,
        "answer_3A3_student_status":answer_3A3_student_status,
        "third_question_B":test_student.question_3B,
        "answer_3B1":test_answer_student.answer_3B1,
        "answer_3B1_student_id":answer_3B1_student_id,
        "answer_3B1_student_status":answer_3B1_student_status,
        "answer_3B2":test_answer_student.answer_3B2,
        "answer_3B2_student_id":answer_3B2_student_id,
        "answer_3B2_student_status":answer_3B2_student_status,
        "answer_3B3":test_answer_student.answer_3B2,
        "answer_3B3_student_id":answer_3B3_student_id,
        "answer_3B3_student_status":answer_3B3_student_status,
        }
    return render(request, 'main/student_info.html', context=context)

@login_required(login_url='/')
def sociyounger(request):
    school = request.user.profile.school
    context = {
        "school":school,
        "first_question_A":sociyounger_questions["first_question_A"],
        "first_question_B":sociyounger_questions["first_question_B"],
        "second_question_A":sociyounger_questions["second_question_A"],
        "second_question_B":sociyounger_questions["second_question_B"],
        "third_question_A":sociyounger_questions["third_question_A"],
        "third_question_B":sociyounger_questions["third_question_B"],
        }
    if request.method == 'POST':
        first_question_A = request.POST.get("first_question_A") if request.POST.get("first_question_A") != "" else sociyounger_questions["first_question_A"]
        first_question_B = request.POST.get("first_question_B") if request.POST.get("first_question_B") != "" else sociyounger_questions["first_question_B"]
        second_question_A = request.POST.get("second_question_A") if request.POST.get("second_question_A") != "" else sociyounger_questions["second_question_A"]
        second_question_B = request.POST.get("second_question_B") if request.POST.get("second_question_B") != "" else sociyounger_questions["second_question_B"]
        third_question_A = request.POST.get("third_question_A") if request.POST.get("third_question_A") != "" else sociyounger_questions["third_question_A"]
        third_question_B = request.POST.get("third_question_B") if request.POST.get("third_question_B") != "" else sociyounger_questions["third_question_B"]
        students_class = request.POST.get("students_class")
        students_litera = request.POST.get("students_litera")

        created_test = test.objects.create(students_litera=students_litera, students_class=students_class, question_1A=first_question_A, question_1B=first_question_B, question_2A=second_question_A, question_2B=second_question_B, question_3A=third_question_A, question_3B=third_question_B,date = dt.today().strftime('%Y-%m-%d'), school=school)
        return redirect(f"http://127.0.0.1:8000/home/test_link/{created_test.test_id}")

    return render(request, 'main/new_soci_5_6.html', context=context) 

@login_required(login_url='/')
def sociolder(request):
    school = request.user.profile.school
    context = {
        "school":school,
        "first_question_A":sociolder_questions["first_question_A"],
        "first_question_B":sociolder_questions["first_question_B"],
        "second_question_A":sociolder_questions["second_question_A"],
        "second_question_B":sociolder_questions["second_question_B"],
        "third_question_A":sociolder_questions["third_question_A"],
        "third_question_B":sociolder_questions["third_question_B"],
        }
    if request.method == 'POST':
        first_question_A = request.POST.get("first_question_A") if request.POST.get("first_question_A") != "" else sociyounger_questions["first_question_A"]
        first_question_B = request.POST.get("first_question_B") if request.POST.get("first_question_B") != "" else sociyounger_questions["first_question_B"]
        second_question_A = request.POST.get("second_question_A") if request.POST.get("second_question_A") != "" else sociyounger_questions["second_question_A"]
        second_question_B = request.POST.get("second_question_B") if request.POST.get("second_question_B") != "" else sociyounger_questions["second_question_B"]
        third_question_A = request.POST.get("third_question_A") if request.POST.get("third_question_A") != "" else sociyounger_questions["third_question_A"]
        third_question_B = request.POST.get("third_question_B") if request.POST.get("third_question_B") != "" else sociyounger_questions["third_question_B"]
        students_class = request.POST.get("students_class")
        students_litera = request.POST.get("students_litera")

        created_test = test.objects.create(students_litera=students_litera, students_class=students_class, question_1A=first_question_A, question_1B=first_question_B, question_2A=second_question_A, question_2B=second_question_B, question_3A=third_question_A, question_3B=third_question_B,date = dt.today().strftime('%Y-%m-%d'), school=school)
        return redirect(f"http://127.0.0.1:8000/home/test_link/{created_test.test_id}")
    
    return render(request, 'main/new_soci_7_11.html', context=context)

@login_required(login_url='/')
def test_link(request, data):
    school = request.user.profile.school
    context = {
        "school":school,
        "url":str("http://127.0.0.1:8000/student/login/" + str(data))
        }
    return render(request, 'main/test_link.html', context=context)



def student_login(request, data):
    student_test = test.objects.get(test_id=data)
    if request.method == 'POST':
        try:
            student_surname = request.POST.get("surname")
            student_name = request.POST.get("name")
            student_patronymic = request.POST.get("patronymic")
            student_birth_year = request.POST.get("year")
            student_class = request.POST.get("class")
            student_litera = (request.POST.get("litera")).upper()
            student_account = student.objects.get(name=student_name, surname=student_surname, patronymic = student_patronymic, school=student_test.school, class_number=student_class, class_litera=student_litera, birth_year=student_birth_year)
            return redirect(f"http://127.0.0.1:8000/student/test/{data}&{student_account.student_id}")
        except:
            return HttpResponse("Ошибка на стадии входа. Удидитесь что вы имеете право проходить данный тест.")


    context = {
        }
    return render(request, 'student/student_login.html', context=context)

def student_test(request, data):
    test_id = data.split("&")[0]
    student_id = data.split("&")[1]
    test_obj = test.objects.get(test_id=test_id)
    school = test.objects.get(test_id=test_id).school
    students_class = test.objects.get(test_id=test_id).students_class
    students_litera = test.objects.get(test_id=test_id).students_litera
    student_obj = student.objects.get(student_id=student_id)

    students = student.objects.filter(class_number=students_class, class_litera=students_litera)
    students_context = ''
    for i in students:
        st = f"{i.surname} {i.name}/"
        students_context = students_context + st
    students_context = students_context[:-1]

    print(json.dumps(students_context, ensure_ascii=False))

    context = {
        "first_question_A":test_obj.question_1A,
        "first_question_B":test_obj.question_1B,
        "second_question_A":test_obj.question_2A,
        "second_question_B":test_obj.question_2B,
        "third_question_A":test_obj.question_3A,
        "third_question_B":test_obj.question_3B,
        "data": json.dumps(students_context, ensure_ascii=False)
        }
    if request.method == 'POST':
        answer_1A1 = request.POST.get("answer_1A1")
        answer_1A2 = request.POST.get("answer_1A2")
        answer_1A3 = request.POST.get("answer_1A3")
        answer_1B1 = request.POST.get("answer_1B1")
        answer_1B2 = request.POST.get("answer_1B2")
        answer_1B3 = request.POST.get("answer_1B3")
        answer_2A1 = request.POST.get("answer_2A1")
        answer_2A2 = request.POST.get("answer_2A2")
        answer_2A3 = request.POST.get("answer_2A3")
        answer_2B1 = request.POST.get("answer_2B1")
        answer_2B2 = request.POST.get("answer_2B2")
        answer_2B3 = request.POST.get("answer_2B3")
        answer_3A1 = request.POST.get("answer_3A1")
        answer_3A2 = request.POST.get("answer_3A2")
        answer_3A3 = request.POST.get("answer_3A3")
        answer_3B1 = request.POST.get("answer_3B1")
        answer_3B2 = request.POST.get("answer_3B2")
        answer_3B3 = request.POST.get("answer_3B3")
        test_answers = test_answer(gender = (student_obj.gender).lower(), patronymic = student_obj.patronymic, surname = student_obj.surname, name = student_obj.name, students_litera=students_litera, students_class=students_class, date=dt.today().strftime('%Y-%m-%d'), student_id=student_id, student_status="None", school=school, test_id=test_id,answer_1A1=answer_1A1,answer_1A2=answer_1A2,answer_1A3=answer_1A3,answer_1B1=answer_1B1,answer_1B2=answer_1B2,answer_1B3=answer_1B3,answer_2A1=answer_2A1,answer_2A2=answer_2A2,answer_2A3=answer_2A3,answer_2B1=answer_2B1,answer_2B2=answer_2B2,answer_2B3=answer_2B3,answer_3A1=answer_3A1,answer_3A2=answer_3A2,answer_3A3=answer_3A3,answer_3B1=answer_3B1,answer_3B2=answer_3B2,answer_3B3=answer_3B3)
        test_answers.save()
        return HttpResponse("Тест завершен!")

    return render(request, 'student/student_test.html', context=context)