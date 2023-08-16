from django.shortcuts import render
from django.contrib.auth import get_user
from profiles_user.models import UsersTelegram, SaleWeapons
from django.http import HttpResponsePermanentRedirect, HttpResponse, HttpResponseRedirect
from weapons.models import Weapons
import requests



def index(request):
    if request.user.is_authenticated:
        user = get_user(request)
        tg_user = UsersTelegram.objects.get(tg_id=int(user.username))
        response = requests.get(f'http://127.0.0.1:5000/get?username={tg_user.username}')
        res = response.json()
        balance = res['balance']
        # balance = 0

        inv = SaleWeapons.objects.filter(user_id=tg_user.tg_id, sale=False)
        ws = []

        print(len(inv))

        for i in inv:
            weapons = Weapons.objects.get(id=i.weapon_id)
            ws.append({
                'id': weapons.id,
                'prod_id': i.id,
                'name': weapons.name,
                "img": weapons.img,
                "model_w": weapons.model_w,
                "price": weapons.price,
                'leg': weapons.leg,
            })
            print(i)
    else:
        tg_user = []
        balance = 0

    return render(request, 'profile.html', {'tg_user': tg_user, 'balance': balance, 'inventory': ws})


def sale(request, id):
    user = get_user(request)
    tg_user = UsersTelegram.objects.get(tg_id=int(user.username))

    if int(id) == 0:
        inv = SaleWeapons.objects.filter(user_id=int(user.username), sale=False)

        for i in inv:
            sw = SaleWeapons.objects.get(id=i.id)
            sw.sale = True
            sw.save(update_fields=["sale"])

            weapon = Weapons.objects.get(id=sw.weapon_id)
            response = requests.get(f'http://127.0.0.1:5000/sale?username={tg_user.username}&plus={weapon.price}')
            res = response.json()

        return HttpResponseRedirect('/profile')

    else:
        sw = SaleWeapons.objects.get(id=int(id))
        sw.sale = True
        sw.save(update_fields=["sale"])

        weapon = Weapons.objects.get(id=sw.weapon_id)
        response = requests.get(f'http://127.0.0.1:5000/sale?username={tg_user.username}&plus={weapon.price}')
        res = response.json()

        return HttpResponsePermanentRedirect('/profile')



