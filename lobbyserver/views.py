from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .my_api import *
from .sockets_deals import create_game,joinGame
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt,requires_csrf_token
from django.http import HttpResponse
from django.middleware.csrf import get_token
import json
# Create your views here.
@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    #resp = JsonResponse({'csrfToken': request.COOKIES['XSRF-TOKEN']})
    resp = JsonResponse({'csrfToken': csrf_token})
    return resp

@jwt_required
def ping(request):
    #authenticate(request, username=username, password=password)
    data=UserSerializer(User.objects.get(username='orwund'))

    '''headers = {"Access-Control-Allow-Origin":"*",
               "Access-Control-Allow-Credentials": "true",
               "Access-Control-Allow-Methods":"GET,HEAD,OPTIONS,POST,PUT",
                "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"}
    '''
    response = JsonResponse(data.data)
    return response

def ping2(request):
    return HttpResponse()

def join_game(request,game_id):
    exists=False
    if joinGame(game_id):
        exists=True
    return JsonResponse({'exists':exists})

@csrf_exempt
@jwt_required
def create_game_view(request,typeg='free'):
    params = request.POST
    try:
        time1={'base':int(params['time1base']),'add':int(params['time1add'])}
    except:
        time1=None
    try:
        time2 = {'base': int(params['time2base']), 'add':int(params['time2add'])}
    except:
        time2 = None
    if typeg == 'free':
        id=create_game(time1,time2)
        return JsonResponse({'game_id':id})
    else:
        return HttpResponse(status=401)



'''@jwt_required
def host_free_game(request):
    id = create_game()
    if id:
        return JsonResponse({'gameid':id})
    else:
        return HttpResponse(status=401)'''