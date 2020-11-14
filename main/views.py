import json

from django.http import JsonResponse
from django.shortcuts import render


def remove_keys(data, back='fio_teach', keys=('id_form', 'form_name', 'fio_teach')):
    value = data.get(back)
    for key in keys:
        del data[key]

    return value


# Create your views here.
def index(request):
    return render(request, 'index.html')


def comments(request):
    return render(request, 'comment_index.html')


def student_passwords(request):
    return render(request, 'password_index.html')


def homework(request):
    return render(request, 'homework_index.html')


def contact(request):
    return render(request, 'contact_us_index.html')


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
