from django.shortcuts import render
#from django.contrib import auth
from lobbychessserver.settings import SECRET_KEY
from ..models import *
from ..my_api import *
from django.contrib.auth import authenticate
#from forum.forms import RegistrationForm
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.mail import send_mail,EmailMultiAlternatives
#from rest_framework.response import Response
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.template.loader import render_to_string
import re

def my_json_response(state,data={}):
    if state:
        data['applied']=True
    else:
        data['applied']=False
    return JsonResponse(data)

class RegistrationView(View):
    '''def get(self,request):
        form = RegistrationForm()
        ctx={'form':form}
      #  send_verification_email(request.user,request.META['HTTP_HOST'])
      #  send_mail('Hello', 'World', 'michael.ufaev@gmail.com', ['michael.ufaev@yandex.ru'])
        #print(request.META)
        #REMOTE_ADDR
        #HTTP_HOST
        return render(request,'registration/registration_form_template.html',context=ctx)'''
    def post(self,request):
        username = request.POST['user_name']
        if not validate('user_name',username):
            return my_json_response(False,{})
        email=request.POST['email']
        if not validate('email',email):
            return my_json_response(False,{})
        password=request.POST['password']
        if not validate('password',password):
            return my_json_response(False,{})
        user=User.objects.create_user(username,email,password)
        user.account = Account.objects.create(rating=1000,user=user)
        user.account.save()
#
#        user = auth.authenticate(username=username, password=password)
#        if user is not None and user.is_active:
#        login(request, user)
#
        return my_json_response(True,{})

def authorisation(request):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        encoded_jwt = jwt.encode(UserSerializer(user).data, SECRET_KEY, algorithm="HS256")
        return JsonResponse({'token':encoded_jwt})
    else:
        return HttpResponse(status=401)

def same_login_req(request):
    if same_login(request):
        return JsonResponse({'exists':True})
    else:
        return JsonResponse({'exists':False})

def same_email_req(request):
    if same_email(request):
        return JsonResponse({'exists':True})
    else:
        return JsonResponse({'exists':False})

def same_login(request):
    new_login= request.GET['login']
    user = User.objects.filter(username=new_login)
    if user:
        return False
    else:
        return True


def same_email(request):
    new_email= request.GET['email']
    email = User.objects.filter(email = new_email)
   # print(user)
    if email:
        return False
    else:
        return True


#def test_json(request):
#    article = Theme.objects.get(pk=1)
#    return JsonResponse(model_to_dict(article))
def validate(name,value):
    if not value:
        return False
    router = {'user_name':[lambda x: length_req(x,5),is_login_free],'email':[is_email,is_email_free],
              'password':[lambda x: length_req(x,8),has_Aa,has_9]}
    for i in router[name]:
        if not i(value):
            return False
    return True

def length_req(value,length):
    if len(value) >= length:
        return True


def is_login_free(value):
    user = User.objects.filter(username=value)
    if not user:
        return True


def is_email_free(value):
    user = User.objects.filter(email=value)
    if not user:
        return True


def is_email(value):
    match = re.match(r'\S+@\S+\.\S+',value).group(0)
  #  print(match)
    if match == value:
        return True

def has_Aa(value):
    result1=re.search(r'[A-Z]',value)
    result2=re.search(r'[a-z]',value)
    if result1.group(0) and result2.group(0):
        return True


def has_9(value):
    result = re.search(r'[0-9]',value)
    if result.group(0):
        return True


def create_token(user):
    return md5(user.password[:5].encode()).hexdigest()


def send_verification_email(user,domen):
    token=create_token(user)
 #   print(domen)
   # print(type(domen))
 #   print(token)
    href= f"http://{domen}/verification/{user.id}/{token}"
    ctx = {'domen':domen,'user_id':user.id,'token':token,'href':href}
  #  message = render_to_string('registration/verification_email.html',context=ctx)
  #  message=template.render(ctx)
   # send_mail('verification',message,'michael.ufaev@gmail.ru',[user.email])
    html_content = render_to_string(
        'registration/verification_email.html',
        ctx
    )
    msg = EmailMultiAlternatives('verification', 'text_content', 'michael.ufaev@gmail.ru', [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def verification_view(request,id,token):
    user = User.objects.get(pk=id)
#    print(token)
    if user.userproperties.verified:
        return HttpResponseRedirect('/')
    true_token=create_token(user)
#    print(true_token)
    if token == true_token:
        user.userproperties.verified=True
        user.userproperties.save()
        ctx={'success':True}
        return render(request,'registration/success.html',context=ctx)
    else:
        return render(request,'registration/success.html',context={'success':False})


def make_verif(request,id):
    user = User.objects.get(pk=id)
    send_verification_email(user, request.META['HTTP_HOST'])
   # return HttpResponseRedirect('/')
    return render(request,'registration/uvedomlenie.html')






