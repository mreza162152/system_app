import os
import re
from datetime import datetime

from django.shortcuts import render
from collections import defaultdict
from .models import Charts


# Create your views here.
def index(request):
    return render(request, 'system_app/index.html')


def load_data(request):
    module_dir = os.path.dirname('D://Visual Exercise//Django//charts_venv//')  
    file_path = os.path.join(module_dir, 'test.txt')  

    date_pattern = "[A-Za-z]{3} \d\d \d\d:\d\d:\d\d"
    category_pattern = "(?<=elk-anis-test )[A-Z a-z\-]*"
    message_pattern = "(?<=elk-anis-test )[A-Z a-z\-].*"

    # data_dict = defaultdict(list)

    with open(file_path) as tf:
        lines = tf.readlines()
        for line in lines:
            date = re.findall(date_pattern, line)
            date_string = date[0]
            date_string = "2021 "+date_string
            date_obj = datetime.strptime(date_string, "%Y %b %d %H:%M:%S")
            # data_dict['date'].append(date_obj)
            # print(date, end='\t')
            category = re.findall(category_pattern, line)
            category = category[0]
            # data_dict['category'].append(category)
            # print(category, end="\t")
            extra_message = re.findall(message_pattern, line)
            extra_message = extra_message[0]
            space_index = extra_message.index(' ')
            pure_message = extra_message[space_index+1:]
            # data_dict['message'].append(pure_message)
            # print(pure_message)

            data = Charts(log_date = date_obj, log_category = category, message = pure_message)
            data.save()
            # context = {'data_dict':data_dict}
    return render(request, 'system_app/load_data.html')


def show_data(request):
    all_data = Charts.objects.all()
    all_data = all_data[:10]
    context = {'all_data':all_data}
    print(all_data)
    return render(request, 'system_app/show_data.html', context)