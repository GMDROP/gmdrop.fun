from django.shortcuts import render
from .forms import *
from weapons.models import *
from .models import *
import json
from profiles_user.models import UsersTelegram, SaleWeapons
from django.contrib.auth import get_user
from django.http import JsonResponse, HttpResponseRedirect
import requests
import random
import json


def case_create(request):
    # if request.method == "POST":
        # form = Case(
        #     name=request.POST.get('name'),
        #     price=request.POST.get('price'),
        #     img=request.FILES[request.POST.get('img')],
        #     weapons=json.loads(request.POST.get('weapons'))
        #
        # )
        # form.save()
        # form = CaseForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
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


def case(request, id):
    case_p = Case.objects.get(id=id)
    ws = []
    for w in case_p.weapons:
        weapons = Weapons.objects.get(id=w['id_weapon'])
        ws.append({
            'id': weapons.id,
            'name': weapons.name,
            "img": weapons.img,
            "model_w": weapons.model_w,
            "price": weapons.price,
            'leg': weapons.leg,
            'chance': w['chance'] - random.randint(0, 10),
            'stattrak': weapons.stattrak
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

    return render(request, 'case.html', {'weapons': ws, 'case': case_p, 'tg_user': tg_user, 'balance': balance})


def get_price(request, id):
    user = get_user(request)
    tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
    response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
    res = response.json()
    balance = res['balance']
    case_p = Case.objects.get(id=id)
    wh = True
    ws = []
    wi = 0 

    for w in case_p.weapons:
        weapons = Weapons.objects.get(id=w['id_weapon'])
        ws.append({
            'id': weapons.id,
            'id_arr': wi,
            'chance': w['chance']
        })

        wi += 1

    rand = random.randint(6, 10*10)
    arrL = random.randint(1, len(ws))

    if case_p.price <= balance:
        while wh == True:
            for i in ws:
                if random.randint(6, 10000) <= i['chance']:
                    item = i['id_arr']
                    id_w = i['id']
                    wh = False
                    break

        resp = requests.get(f'http://127.0.0.1:5000/update?username={tg_user.username}&minus={case_p.price}')
        re = resp.json()
        bal = res['balance']
        ws = []
        inventory = SaleWeapons(
            user_id=tg_user.tg_id,
            weapon_id=id_w,
            sale=False
        )
        inventory.save()

        inv = SaleWeapons.objects.filter(user_id=tg_user.tg_id, sale=False)
        for i in inv:
            ws.append({
                'id': i.id
            })

    else:
        item = 0

    return JsonResponse({
        'item': item,
        'sw_id': ws[-1]['id']
    })
