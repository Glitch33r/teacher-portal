import json
import random

import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render
from .logbook_connection import LogbookBot
from django.views.decorators.csrf import csrf_exempt
from .models import *
from decouple import config


def remove_keys(data, back='fio_teach', keys=('id_form', 'form_name', 'fio_teach')):
    value = data.get(back)
    for key in keys:
        del data[key]

    return value


# Create your views here.
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def comments(request):
    bot = LogbookBot()
    if request.is_ajax():
        if request.POST.get('type') == 'login':
            login = request.POST.get('login')
            password = request.POST.get('password')
            if bot.login(login, password):
                html = render_to_string('comment_form.html', {'groups': bot.get_groups()})
                return HttpResponse(html)
            else:
                error = 'Проверьте правильность введенного логина и пароля.'
                return JsonResponse({'error': error}, status=400)
        elif request.POST.get('type') == 'group':
            group_id = request.POST.get('group')
            html = render_to_string('comment_parts/option_student.html',
                                    {'students': bot.get_students_of_group(group_id)})
            return HttpResponse(html)
        elif request.POST.get('type') == 'student':
            student_id = request.POST.get('student')
            html = render_to_string('comment_parts/option_subject.html',
                                    {'subjects': bot.get_subjects_for_group(student_id)})
            return HttpResponse(html)
        elif request.POST.get('type') == 'generate':
            criteria = request.POST.get('criteria')
            print(criteria == '')
            text = ''
            if criteria != '':
                for slug in criteria.split(','):
                    btn_id = Buttons.objects.get(slug=slug).id
                    phrases = Phrase.objects.filter(button_id=btn_id, lang='ru')
                    phrase = random.choice(phrases)
                    text += phrase.text + '. '
                return HttpResponse(text)
            else:
                html = error_handling('Ошибка', 'Произошла ошибка. Не выбраны критерии для генерации.')
                return HttpResponse(html, status=400)
        elif request.POST.get('type') == 'send':
            group_id = request.POST.get('group')
            student_id = request.POST.get('student')
            subject_id = request.POST.get('subject')
            text = request.POST.get('comment')
            send = bot.send_comment(group_id, student_id, subject_id, text)
            if send:
                html = error_handling('Успех!', 'Комментарий добавлен!')
                return HttpResponse(html)
            else:
                html = error_handling('Ошибка',
                                      'Произошла ошибка. Проверьте данные и попробуйте еще раз. '
                                      'Или обратитесь к администратору.')
                return HttpResponse(html)

    return render(request, 'comment_index.html')


def error_handling(title, msg):
    return render_to_string('modal.html', {'title': title, 'msg': msg})


@csrf_exempt
def student_passwords(request):
    bot = LogbookBot()
    if request.is_ajax():
        if request.POST.get('type') == 'login':
            login = request.POST.get('login')
            password = request.POST.get('password')
            if bot.login(login, password):
                html = render_to_string('password_group_select.html', {'data': bot.get_groups()})
                return HttpResponse(html)
            else:
                error = 'Проверьте правильность введенного логина и пароля.'
                return JsonResponse({'error': error}, status=400)
        elif request.POST.get('type') == 'group':
            group_id = request.POST.get('group')
            html = render_to_string('password_student_select.html', {'data': bot.get_students_of_group(group_id)})
            return HttpResponse(html)

    return render(request, 'password_index.html')


def homework(request):
    return render(request, 'homework_index.html')


@csrf_exempt
def contact(request):
    if request.is_ajax():
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('message')

        msg = f"От: <b>{name}</b>\nEmail: <b>{email}</b>\nText:\n{text}"

        answ = telegram_bot_sendtext(msg)
        print(answ)
        html = error_handling('Успех!', 'Комментарий добавлен!')
        return HttpResponse(html)

    return render(request, 'contact_us_index.html')


def telegram_bot_sendtext(bot_message):
    token = config('TG_TOKEN')
    chat_id = config('TG_CHAT_ID')
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def load_file_to_db(request):
    if request.method == 'POST':
        file = request.FILES['myFile']
        file = json.loads(file.read())

        teacher_dict = {}
        for study_type, value in file['report'].items():
            for v in value.values():
                month = v.get('month')
                teacher_dict.update({
                    month.get('fio_teach'): {}
                })

        for study_type, value in file['report'].items():
            for v in value.values():
                temp_dict = {}
                month = v.get('month')
                fio_teach = remove_keys(month)
                temp_dict.update({'month': month})
                if 'week' in v:
                    week = v.get('week')
                    remove_keys(week)
                    temp_dict.update({'week': week})

                teacher_dict[fio_teach].update({
                    study_type: temp_dict
                })

        return JsonResponse({'status': True})
    else:
        return render(request, 'load_file_to_db_form.html')
