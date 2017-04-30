from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from athena.models import RTLS_times, EHR_times
import athenahealthapi
import time
import datetime
import json


appt_statuses = {'x': 'cancelled', 'f': 'future', 'o': 'open', '2': 'checked in', '3': 'checked out', '4': 'charge entered'}
key = 'm4ycke3bt6y4yss6wrnctma5'
secret = 'Uqe3Rke2QtX5K5R'
version = 'preview1'
practiceid = 1959343

api = athenahealthapi.APIConnection(version, key, secret, practiceid)

api.POST('/appointments/changed/subscription/events')

def index(request):
    return render(request, 'athena/index.html')

def get_times(request):
    appointment = api.GET('/appointments/changed')

    for appt in appointment['appointments']:
        loc = ""
        if 'patientlocationid' in appt: loc = get_rooms(appt['patientlocationid'])
        EHR_times.objects.create(interaction_id=1, times=timezone.now(), status=appt['appointmentstatus'], location=loc)

    context = get_context()
    return render(request, 'athena/times.html', context)

def path_join(*parts):
    return ''.join('/' + str(part).strip('/') for part in parts if part)

def get_rooms(id):
    locations = api.GET('/misc/patientlocations')
    loc_index = next(index for (index, d) in enumerate(locations) if d['patientlocationid'] == int(id))
    return locations[loc_index]['name']

def get_status(id):
    return appt_statuses[id]

def get_context():
    rtls_obj = RTLS_times.objects.order_by('times')
    ehr_obj = EHR_times.objects.order_by('times')

    ehr_count = 0
    rtls_count = 0
    ehr_times = []
    rtls_times = []

    for slot in range(0, len(rtls_obj) + len(ehr_obj)):
        if rtls_count == len(rtls_obj):
            obj = ehr_obj[ehr_count]
            ehr_times.append(obj.location + " : " + get_status(obj.status) + " : " +  obj.times.strftime('%H:%M:%S'))
            rtls_times.append("")
            ehr_count += 1
            continue
        elif ehr_count == len(ehr_obj):
            obj = rtls_obj[rtls_count]
            ehr_times.append("")
            rtls_times.append(obj.times.strftime('%H:%M:%S') + " : " + obj.location)
            rtls_count += 1
            continue

        if rtls_obj[rtls_count].times > ehr_obj[ehr_count].times:
            obj = ehr_obj[ehr_count]
            ehr_times.append(obj.location + " : " + get_status(obj.status) + " : " + obj.times.strftime('%H:%M:%S'))
            rtls_times.append("")
            ehr_count += 1
        else:
            obj = rtls_obj[rtls_count]
            ehr_times.append("")
            rtls_times.append(obj.times.strftime('%H:%M:%S') + " : " + obj.location)
            rtls_count += 1

    return {'rtls_times': rtls_times, 'ehr_times': ehr_times}
