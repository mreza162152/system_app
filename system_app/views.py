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

######### PIE

    pie_data_dict = defaultdict(int)
    pie_all_data = Charts.objects.all()
    for i in pie_all_data:
        category = i.log_category
        pie_data_dict[category] +=1

    pie_keys = pie_data_dict.keys()
    pie_keys = list(pie_keys)
    pie_values = pie_data_dict.values()
    pie_values = list(pie_values)

    data_list = []
    for i in range(len(pie_keys)):
        data_list.append({'name': pie_keys[i], 'y': pie_values[i]})

###### TIMELINE

    time_data_dict = defaultdict(int)
    time_all_data = Charts.objects.all()
    for i in time_all_data:
        date_string = i.log_date.strftime("%m-%d %H:%M:%S")
        time_data_dict[date_string] +=1

    time_keys = time_data_dict.keys()
    time_keys = list(time_keys)
    time_keys.insert(0, 'Date')
    time_values = time_data_dict.values()
    time_values = list(time_values)
    time_values.insert(0,'Total Messages')

####### DATA TABLE
 

    table_all_data = Charts.objects.all()
    table_all_data = table_all_data[:10]

    context = {'data_list' : json.dumps(data_list), 'time_values':time_values, 'time_keys':time_keys, 'table_all_data':table_all_data}
    return render(request, 'system_app/show_data.html', context)
