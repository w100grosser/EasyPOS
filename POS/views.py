import json

from django.db.models.fields import DateField
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import Item, sellReceipt


def show(request):
    latest_item_list = Item.objects.order_by('-add_date')[:5]
    context = {'latest_item_list': latest_item_list}
    return render(request, 'POS/show.html', context)


def sell(request):
    return render(request, 'POS/sell.html')


def detail(request, item_id):
    return HttpResponse("توكل على الله %s." % item_id)


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
    item_bar = request.GET.get('bar', 0)
    data = {
        'name': Item.objects.filter(bar=item_bar)[0].name, 'price': Item.objects.filter(bar=item_bar)[0].price
    }
    print('got item')
    return JsonResponse(data)


def submit_receipt(request):

    itemsl = json.loads(request.POST['itemsl'])

    try:
        sellReceipt_i = sellReceipt(add_date=timezone.now())
        sellReceipt_i.name = str(sellReceipt.objects.last().id+1)
        sellReceipt_i.items = itemsl
        sellReceipt_i.amount = sum(
            [float(itemsl[x]['price'])*float(itemsl[x]['Ni']) for x in itemsl.keys()])
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

# Create your views here.
