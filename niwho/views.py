#encode=utf8

import json
import hashlib

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def temp_verify(request):
    sp = {
        'nonce': request.GET['nonce'],
        'timestamp': request.GET['timestamp'],
        'token ': 'niwho1266',
    }
    msg = ''.join(sorted([v for v in sp.values()]))
    if hashlib.sha1(msg).hexdigest() == request.GET['signature']:
        return HttpResponse(request.GET['echostr'])

def index(request):
    return render(request, 'niwho/index.html')
# Create your views here.
@csrf_exempt
def info(request):
    data=[
            {'name': 'aaa', 'price':99, 'ot':[1,2,3]},
            {'name':'bbb', 'price':67, 'ot':[4,5,6]},
            {'name': 'ccc', 'price': 111, 'ot':[7,8,9]},
            {'name': 'ccc', 'price': 111, 'ot':[7,8,9]},
            {'name': 'ccc', 'price': 111, 'ot':[7,8,9]},
            {'name': 'ccc', 'price': 111, 'ot':[7,8,9]},
            {'name': 'ccc', 'price': 111, 'ot':[7,8,9]},
         ]
    return HttpResponse(json.dumps(data), content_type="application/json")
