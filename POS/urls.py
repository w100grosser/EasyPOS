from django.urls import path
from django.conf.urls import url

from . import views


app_name = 'POS'

urlpatterns = [
    # path('', views.sell, name='sell'),
    path('sell', views.sell, name='sell'),
    path('buy', views.buy, name='buy'),
    path('home', views.home, name='home'),
    path('changeitem', views.changeitem, name='changeitem'),
    path('sales231111', views.sales, name='sales231111'),
    path('item/<int:item_id>/', views.detail, name='detail'),
    path('sell/<int:sellReceipt_id>/', views.addsell, name='addsell'),
    path('sell/jquery-3.6.0.min.js/', views.jsload, name='jsload'),
    url(r'^ajax/validate_username/$',
        views.validate_username, name='validate_username'),
    url(r'^ajax/get_item/$', views.get_item, name='get_item'),
    url(r'^ajax/submit_receipt/$', views.submit_receipt, name='submit_receipt'),
    url(r'^ajax/submit_receipt_buy/$', views.submit_receipt_buy, name='submit_receipt_buy'),
    url(r'^ajax/change_item/$', views.change_item, name='change_item'),
    url(r'^ajax/addfiles/$', views.addfiles, name='addfiles'),
    url(r'^ajax/getsales/$', views.getsales, name='getsales'),
    #path('/sellReceipt/<int:sellReceipt_id>/', views.addsell, name='sellReceipt'),
]
