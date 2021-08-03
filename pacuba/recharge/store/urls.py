from django.urls import path
from store.views import get_cell_offers, get_nauta_offers,\
payment_done, payment_canceled, IndexView, RechargeView, PayView, ContactoView

urlpatterns = [
    path('',IndexView.as_view(), name="index"),
    path('get_cell_offers/', get_cell_offers, name="get_cell_offers"),
    path('get_nauta_offers/', get_nauta_offers, name="get_nauta_offers"),
    path('recharge/', RechargeView.as_view(), name="recharge"),
    path('pay/', PayView.as_view(), name="pay"),
    path('payment-done/', payment_done, name='payment_done'),
    path('contact-us/', ContactoView.as_view(), name='contact-us'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]