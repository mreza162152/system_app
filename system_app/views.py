import os
import re
from datetime import datetime
import csv
import json

from django.shortcuts import render
from collections import defaultdict
from datetime import datetime
from .models import Charts

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'system_app/index.html')

@login_required
def load_data(request):
    module_dir = os.path.dirname('D://Visual Exercise//Django//charts_venv//')  
    file_path = os.path.join(module_dir, 'log.txt')  

    date_pattern = "[A-Za-z]{3} \d\d \d\d:\d\d:\d\d"
    category_pattern = "(?<=elk-anis-test )[A-Z a-z\-]*"
    message_pattern = "(?<=elk-anis-test )[A-Z a-z\-].*"


    with open(file_path) as tf:
        lines = tf.readlines()
        for line in lines:
            date = re.findall(date_pattern, line)
            date_string = date[0]
            date_string = "2021 "+date_string
            date_obj = datetime.strptime(date_string, "%Y %b %d %H:%M:%S")

            category = re.findall(category_pattern, line)
            category = category[0]
            
            extra_message = re.findall(message_pattern, line)
            extra_message = extra_message[0]
            space_index = extra_message.index(' ')
            pure_message = extra_message[space_index+1:]

            data = Charts(log_date = date_obj, log_category = category, message = pure_message)
            # data.save()

    return render(request, 'system_app/load_data.html')


@login_required
def show_data(request):
    all_data = Charts.objects.all()
    all_data = all_data[:10]
    context = {'all_data':all_data}
    return render(request, 'system_app/show_data.html', context)


def data_timeline(request):
    data_dict = defaultdict(int)
    all_data = Charts.objects.all()
    for i in all_data:
        date_string = i.log_date.strftime("%m-%d %H:%M:%S")
        # print(date_string)
        data_dict[date_string] +=1
    keys = data_dict.keys()
    keys = list(keys)
    values = data_dict.values()
    values = list(values)
    # with open('dict.csv', 'w') as csv_file:  
    #     writer = csv.writer(csv_file)
    #     for key, value in data_dict.items():
    #         writer.writerow([key, value])  

    context = {'keys':keys, 'values':values}
    return render(request, 'system_app/data_timeline.html', context)



def data_pie(request):
    data_dict = defaultdict(int)
    all_data = Charts.objects.all()
    for i in all_data:
        category = i.log_category
        data_dict[category] +=1
    keys = data_dict.keys()
    keys = list(keys)
    values = data_dict.values()
    values = list(values)

    data_list = []
    for i in range(len(keys)):
        data_list.append({'name': keys[i], 'y': values[i]})
    print(type(data_list[1]))
    # data_dict = dict(data_dict)
    # context = {'keys':keys, 'values':values}
    # context = {'data_dict' : data_dict}

    context = {'data_list' : json.dumps(data_list)}
    return render(request, 'system_app/data_pie.html', context)
