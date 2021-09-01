import os
import re
from datetime import datetime

from django.shortcuts import render
from collections import defaultdict
from datetime import datetime
from .models import Charts

from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'system_app/index.html')

@login_required
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

@login_required
def show_data(request):
    all_data = Charts.objects.all()
    all_data = all_data[:10]
    context = {'all_data':all_data}
    print(all_data)
    return render(request, 'system_app/show_data.html', context)


def data_timeline(request):
    data_dict = defaultdict(int)
    all_data = Charts.objects.all()
    for i in all_data:
        date_string = i.log_date.strftime("%m-%d %H:%M:%S")
        print(date_string)
        data_dict[date_string] +=1
    keys = data_dict.keys()
    keys = list(keys)
    values = data_dict.values()
    values = list(values)

    context = {'keys':keys, 'values':values}
    return render(request, 'system_app/data_timeline.html', context)



def data_pie(request):
    data_dict = defaultdict(int)
    all_data = Charts.objects.all()
    for i in all_data:
        category = i.log_category
        data_dict[category] +=1
    # keys = data_dict.keys()
    # keys = list(keys)
    # values = data_dict.values()
    # values = list(values)
    print(data_dict)
    data_dict = dict(data_dict)
    # context = {'keys':keys, 'values':values}
    context = {'data_dict' : data_dict}
    return render(request, 'system_app/data_pie.html', context)
