import json

from django.shortcuts import render
from django_telegram_login.widgets.constants import (
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import create_redirect_login_widget
from django.conf import settings
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from profiles_user.models import UsersTelegram
from case.models import Case
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user
from django.http import JsonResponse
import sqlite3
import requests
from weapons.models import *
from django.views.generic import DetailView, UpdateView
from case.forms import *
from weapons.forms import *


bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL
DATABASE = '../../data.db'


def home(request):
    telegram_login_widget = create_redirect_login_widget(
        redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
    )

    cat_1 = Categories.objects.all()

    num = 1

    cat_arr = []

    for cs in cat_1:
        cat = Categories.objects.filter(position=num)

        num += 1
        
        for c in cat:
            name = c.name
            cases = c.cases_arr
            cases_array = []
            for case in cases:
                cas = Case.objects.get(id=case['id'])
                cases_array.append({
                    'id': cas.id,
                    'name': cas.name,
                    "img": cas.img,
                    "price": cas.price,
                    'weapons': cas.weapons,
                })
            cat_arr.append({
                'id': c.id,
                'name': name,
                "cases_array": cases_array,
            })

    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        # balance = 0
    else:
        tg_user = []
        balance = 0

    # con = sqlite3.connect("../../data.db")
    # cur = con.cursor()
    # res = cur.execute(f"SELECT balance FROM users WHERE username='{tg_user.username}'")
    # balance = res.fetchone()

    context = {'telegram_login_widget': telegram_login_widget, 'cases': cat_arr, 'tg_user': tg_user, 'balance': balance}
    return render(request, 'home.html', context=context)


def get_balance(request):
    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        # balance = 0
    else:
        tg_user = []
        balance = 0

    return JsonResponse({
            'balance': balance,
        })


def auth(request):
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(bot_token=bot_token, request_data=request.GET,)
        tg_users = UsersTelegram.objects.filter(tg_id=request.GET.get('id'))
        user_check = User.objects.filter(username=request.GET.get('id'))
        if not tg_users:
            create_tg_users = UsersTelegram(
                tg_id=request.GET['id'],
                first_name=request.GET['first_name'],
                username=request.GET['username'],
                photo_url=request.GET['photo_url'],

            )
            create_tg_users.save()

        UsersTelegram.objects.filter(id=request.GET.get('id')).update(photo_url=request.GET['photo_url'])

        if not user_check:
            create_user = User.objects.create_user(request.GET.get('id'), '', request.GET.get('id'))
            create_user.first_name = request.GET['first_name']
            create_user.save()

        user = authenticate(username=request.GET.get('id'), password=request.GET.get('id'))
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponsePermanentRedirect('/')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')

    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

        # Or handle it as you wish. For instance, save to DB.
    # return cookie_site

def personal_admin(request):
    if request.user.is_superuser:
        cases = Case.objects.all()

        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']

        context = {'tg_user': tg_user, 'cases': cases, 'balance': balance}
        return render(request, 'personal-admin.html', context=context)
    else:
        return HttpResponseRedirect('/')

# def personal_admin_cases(request, id):
#     if request.user.is_superuser:
#         cases = Case.objects.all()
# 
#         user = get_user(request)
#         tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
#         response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
#         res = response.json()
#         balance = res['balance']
# 
#         context = {'tg_user': tg_user, 'cases': cases, 'balance': balance}
#         return render(request, 'personal_admin_cases.html', context=context)
#     else:
#         return HttpResponseRedirect('/')

def case_create(request):
    if request.method == 'POST':
        cf = CaseForm(request.POST or None, request.FILES or None)
        if cf.is_valid():
            product = cf.save(commit=False)
            product.save()
            # return HttpResponseRedirect('/case/create/')

    form = CaseForm()
    weapons = Weapons.objects.all()

    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        # balance = 0
    else:
        tg_user = []
        balance = 0
    return render(request, 'createcase.html', {'form': form, 'weapons': weapons, 'tg_user': tg_user, 'balance': balance})

def weapon_create(request):
    if request.method == 'POST':
        cf = WeaponsForm(request.POST or None, request.FILES or None)
        if cf.is_valid():
            product = cf.save(commit=False)
            product.save()
            # return HttpResponseRedirect('/case/create/')

    form = WeaponsForm()

    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        # balance = 0
    else:
        tg_user = []
        balance = 0
    return render(request, 'personal_admin_weapons_create.html', {'form': form, 'tg_user': tg_user, 'balance': balance})
    
class CaseUpdate(UpdateView):
    model = Case
    template_name = 'personal_admin_cases.html'

    fields = ['name', 'price', 'img', 'weapons']


    def get_context_data(self, *args, **kwargs):
        ws = []

        w = Weapons.objects.all()

        for weapons in w:
            ws.append({
                'id': weapons.id,
                'name': weapons.name,
                "img": weapons.img,
                "model_w": weapons.model_w,
                "price": weapons.price,
                'leg': weapons.leg,
            })

        context = super(CaseUpdate, self).get_context_data(*args, **kwargs)
        context['weapons'] = ws
        return context


class WeaponsUpdate(UpdateView):
    model = Weapons
    template_name = 'personal_admin_weapons_update.html'

    fields = ['name', 'model_w', 'price', 'img', 'leg', 'stattrak']
    

def personal_admin_weapons(request):
    if request.user.is_superuser:
        weapons = Weapons.objects.all()

        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']

        context = {'tg_user': tg_user, 'weapons': weapons, 'balance': balance}
        return render(request, 'personal_admin_weapons.html', context=context)
    else:
        return HttpResponseRedirect('/')


def personal_admin_categories(request):
    if request.user.is_superuser:
        categories = Categories.objects.all()

        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']

        context = {'tg_user': tg_user, 'categories': categories, 'balance': balance}
        return render(request, 'personal_admin_categories.html', context=context)
    else:
        return HttpResponseRedirect('/')

class CategoriesUpdate(UpdateView):
    model = Categories
    template_name = 'personal_admin_categories_update.html'

    fields = ['name', 'position', 'cases_arr']

    def get_context_data(self, *args, **kwargs):
        ws = []
        cat = Categories.objects.get(id=self.kwargs['pk'])
        cases = Case.objects.all()
        for weapons in cat.cases_arr:
            w = Case.objects.get(id=weapons['id'])
            ws.append({
                'id': w.id,
                'name': w.name,
                "img": w.img,
                "price": w.price,
            })

        context = super(CategoriesUpdate, self).get_context_data(*args, **kwargs)
        context['case'] = ws
        context['cases'] = cases
        return context

def categories_create(request):
    if request.method == 'POST':
        cf = CategoriesForm(request.POST or None, request.FILES or None)
        if cf.is_valid():
            product = cf.save(commit=False)
            product.save()
            # return HttpResponseRedirect('/case/create/')

    form = CategoriesForm()

    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        ws = []
        cases = Case.objects.all()

        # balance = 0
    else:
        tg_user = []
        balance = 0
    return render(request, 'personal_admin_categories_create.html', {'form': form, 'case': ws, 'cases': cases, 'tg_user': tg_user, 'balance': balance})