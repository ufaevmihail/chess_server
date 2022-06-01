from django.contrib import admin
from django.urls import path
#from registration_views import registration_views
#import views
from lobbyserver import views
from lobbyserver.registration_views import registration_views
import requests

urlpatterns = [
    path('get_csrf/',views.get_csrf_token),
    path('ping/',views.ping),
    path('ping2/',views.ping2),
    path('join_game/<int:game_id>',views.join_game),
    path('create_game/free/',views.create_game_view),
    path('registration/', registration_views.RegistrationView.as_view()),
    path('exist_login/',registration_views.same_login_req),
    path('exist_email/',registration_views.same_email_req),
    path('auth/',registration_views.authorisation)
]
#print('url')

import threading
import time
def make_req():
    time.sleep(2)
    while True:
        requests.get('https://mychessapplication.herokuapp.com')
        requests.get('https://chess-server-app.herokuapp.com')
        time.sleep(1200)
#threading.Thread(target=make_req).start()