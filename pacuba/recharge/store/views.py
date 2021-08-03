from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Recharge, Contacto
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .forms import RechargeForm, ContactoForm
import json
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.generic import View
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'index.html', context)

class RechargeView(View):
    form = RechargeForm()
    def post(self, request, *args, **kwargs):

        type_recharge = request.POST.get('oculto')
        id_product = request.POST.get('oculto1')
        product = Product.objects.get(pk=int(id_product))
        number_account = request.POST.get('benef')
        user = request.user
        if user.is_authenticated:
            if type_recharge == 'cubacel':
                recharge = Recharge(client= user, product=product, cellphone=number_account)
                recharge.save()
                request.session['recharge_id'] = recharge.id

            else:
                recharge = Recharge(client= user, product=product, nauta=number_account)
                recharge.save()
                request.session['recharge_id'] = recharge.id

            return redirect('pay')
        else:
            return render(request, "index.html")

class PayView(View):
    def get(self, request, *args, **kwargs):   
        if request.user.is_authenticated:
            
            recharge_id = request.session.get('recharge_id')
            recharge = get_object_or_404(Recharge, id=recharge_id)
            host = self.request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '%.2f' % recharge.product.price.quantize(
                    Decimal('.01')),
                'item_name': 'Order {}'.format(recharge.id),
                'invoice': str(recharge.id),
                'currency_code': 'EUR',
                'notify_url': 'http://{}{}'.format(host,
                                                reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,
                                                reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host,
                                                    reverse('payment_cancelled')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {'recharge': recharge, 'form': form}
            return render(request, 'pay.html', context)
        else:
          return render(request, "index.html")

class ContactoView(View):
    form = ContactoForm()
    template_name = "contact.html"

    def get(self, request, * args, ** kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, * args, ** kwargs):
        contact_form = ContactoForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            subject = contact_form.cleaned_data['subject']
            from_email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['mensaje']
            email = send_mail(subject, message,from_email, [settings.EMAIL_HOST_USER])

            return render(request, self.template_name, {'form': self.form})
  

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

@login_required
def get_cell_offers(request):
        products = Product.objects.filter(category__name='Cubacel')
        context = serializers.serialize('json', products, fields=('name','price'))
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required    
def get_nauta_offers(request):
    products = Product.objects.filter(category__name='Nauta')
    context = serializers.serialize('json', products)
    return JsonResponse(context, safe=False)
    
    