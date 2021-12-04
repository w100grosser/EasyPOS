import json

from django.db.models.fields import DateField
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import *

def addfiles(request):
    with open('/root/EasyPOS/POS/bars.txt', 'r') as f:
        for i in f.read().split('\n'):
            try:
                m = i.split(';')
                print(int(float(m[0])),m[1], m[-1])
                bar = int(float(m[0]))
                name = m[-1]
                price = float(m[1])
                item = Item(add_date=timezone.now())
                item.name = name
                item.price = price
                item.stock = 0
                item.bar = bar
                item.save()

            except Exception as e:
                print(e)
                continue

    data = {
        'success': 1
    }
    return JsonResponse(data)


def show(request):
    latest_item_list = Item.objects.order_by('-add_date')[:5]
    context = {'latest_item_list': latest_item_list}
    return render(request, 'POS/show.html', context)


def sell(request):
    return render(request, 'POS/sell.html')


def buy(request):
    return render(request, 'POS/buy.html')


def home(request):
    return render(request, 'POS/home.html')


def changeitem(request):
    return render(request, 'POS/changeitem.html')


def detail(request, item_id):
    return HttpResponse("توكل على الله %s." % item_id)


def change_item(request):
    itemsl = json.loads(request.POST['itemsl'])
    if int(itemsl['bar']) < 1:
        return JsonResponse({
            'success': 0
        })
    if itemsl['newiteml'] == 0:
        try:
            item = Item.objects.get(bar=itemsl['bar'])
            item.name = itemsl['name']
            item.price = float(itemsl['price'])
            item.save()
        except:
            return JsonResponse({
                'success': 0
            })
    else:
        try:
            item = Item(add_date=timezone.now())
            item.bar = int(itemsl['bar'])
            item.price = float(itemsl['price'])
            item.name = itemsl['name']
            item.save()
        except:
            return JsonResponse({
                'success': 0
            })

    return JsonResponse({
        'success': 1
    })


def addsell(request, sellReceipt_id):
    #sellReceipt = get_object_or_404(sellReceipt, pk=sellReceipt_id)
    sellreceipt = sellReceipt.objects.get(id=sellReceipt_id)
    if request.POST.get("item_bar", 0) == '':
        return render(request, 'POS/sell.html', {'sellReceipt': sellreceipt,
                                                 'latest_item_list': page_list(sellreceipt.items),
                                                 'Item': Item,
                                                 })
    else:
        item_bar = int(request.POST.get("item_bar", 0))

    if not Item.objects.filter(bar=item_bar).exists() or item_bar == 0:
        return render(request, 'POS/sell.html', {'sellReceipt': sellreceipt,
                                                 'latest_item_list': page_list(sellreceipt.items),
                                                 'Item': Item,
                                                 })

    #sellreceipt.items['items'] = [{'name' :Item.objects.get(bar = item).name}]
    #sellreceipt.items['items'].append({'name' :Item.objects.get(bar = item).name})
    sellreceipt.items = fill_receipt(sellreceipt.items, Item.objects.filter(
        bar=item_bar)[0].name, item_bar, Item.objects.filter(bar=item_bar)[0].price)
    sellreceipt.save()
    return render(request, 'POS/sell.html', {'sellReceipt': sellreceipt,
                                             'latest_item_list': page_list(sellreceipt.items),
                                             'Item': Item,
                                             })
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # return HttpResponseRedirect(reverse('POS/sell.html', args=(question.id,)))


def fill_receipt(json, name, bar, price):
    if "__" in json['items'].keys():
        return {"items": {name: {"bar": bar, "price": price, "Nsold": 1}}}
    if name in json['items'].keys():
        json["items"][name]["Nsold"] = json["items"][name]["Nsold"] + 1
        return json
    json["items"][name] = {"bar": bar, "price": price, "Nsold": 1}
    return json


def page_list(json):
    if not new_receipt(json):
        return [('Name : ' + x + '\t\tQuantity : ' + str(json['items'][x]['Nsold']) + '\t\tPrice : ' + str(json['items'][x]['price'])) for x in json['items'].keys()]
    return list()


def new_receipt(json):
    if "__" in json['items'].keys():
        return True
    return False


def jsload(request):
    latest_item_list = Item.objects.order_by('-add_date')[:5]
    context = {'latest_item_list': latest_item_list}
    return render(request, 'POS/show.html', context)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': {'i2': '3', 'i1': '3', 'i3': '3'}
    }
    return JsonResponse(data)


def get_item(request):
    print('please')
    item_bar = int(request.GET.get('bar', 0))
    if item_bar < 1:
        return JsonResponse({
            'bar': 0
        })
    print(item_bar)
    try:
        data = {
            'name': Item.objects.filter(bar=item_bar)[0].name, 'price': Item.objects.filter(bar=item_bar)[0].price, 'bar': Item.objects.filter(bar=item_bar)[0].bar
        }
    except:
        return JsonResponse({
            'bar': 0
        })
    print('got item')
    return JsonResponse(data)


def submit_receipt(request):

    itemsl = json.loads(request.POST['itemsl'])
    amount = 0
    try:

        sellReceipt_i = sellReceipt(add_date=timezone.now())
        sellReceipt_i.name = str(sellReceipt.objects.last().id+1)
        sellReceipt_i.items = itemsl

        for i in itemsl.keys():
            amount += float(itemsl[i]['price'])*float(itemsl[i]['Ni'])
            item = Item.objects.get(bar=itemsl[i]['bar'])
            item.stock = item.stock - itemsl[i]['Ni']
            item.save()
        sellReceipt_i.save()

        data = {
            'success': 1
        }
    except:
        data = {
            'success': 0
        }
        return JsonResponse(data)
    return JsonResponse(data)


def submit_receipt_buy(request):

    itemsl = json.loads(request.POST['itemsl'])
    amount = request.POST['amountl']
    print('test', itemsl, amount)
    try:

        buyReceipt_i = buyReceipt(add_date=timezone.now())
        buyReceipt_i.name = str(buyReceipt.objects.last().id+1)
        buyReceipt_i.items = itemsl
        for i in itemsl.keys():
            item = Item.objects.get(bar=itemsl[i]['bar'])
            item.stock = item.stock + itemsl[i]['Ni']
            item.save()
        buyReceipt_i.amount = int(amount)
        buyReceipt_i.save()
        data = {
            'success': 1
        }
    except:
        data = {
            'success': 0
        }
        return JsonResponse(data)
    return JsonResponse(data)

# Create your views here.
