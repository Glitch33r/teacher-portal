from django.urls import path, include
from .views import *

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('homework', homework, name='homework'),
    path('passwords', student_passwords, name='passwords'),
    path('comments', comments, name='comments'),
    path('contact-us', contact, name='contact-us'),
    path('load-file', load_file_to_db, name='load-file')
]
