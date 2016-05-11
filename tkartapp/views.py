from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.forms import ModelForm
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core import serializers
import json
from collections import defaultdict
from decimal import Decimal


from ipdb import set_trace

from .models import Shirt, UserProfile
from .forms import RegistrationForm

class ShirtForm(ModelForm):
    class Meta:
        model = Shirt
        fields = ['name','size','price','description','quantity']


@login_required(login_url='tkartapp:login')
def store(request,template_name = 'store/index.html'):
    shirt = Shirt.objects.all
    data  = {}
    data['shirt_list'] = shirt

    return render(request,template_name,data)

@login_required(login_url='tkartapp:login')
def shirt_list(request,template_name = 'store/admin.html'):
    shirt = Shirt.objects.all
    data  = {}
    data['shirt_list_admin'] = shirt

    return render(request,template_name,data)

def shirt_create(request,template_name= 'store/form.html'):
    form = ShirtForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tkartapp:shirt_list')

    return render(request,template_name,{'form':form})

def shirt_update(request,pk,template_name='store/form.html'):
    shirt = get_object_or_404(Shirt, pk=pk)
    form = ShirtForm(request.POST or None, instance = shirt)
    if form.is_valid():
        form.save()
        return redirect('tkartapp:shirt_list')

    return render(request,template_name,{'form':form})

def shirt_delete(request, pk, template_name='store/delete.html'):
    shirt= get_object_or_404(Shirt, pk=pk)
    if request.method=='POST':
        shirt.delete()
        return redirect('tkartapp:shirt_list')

    return render(request, template_name, {'object':shirt})

def addtocart(request,products={},template_name='store/index.html'):
    pk = request.POST['id']
    name= request.POST['name']
    size = request.POST['size']
    quantity = request.POST['quantity']
    price = request.POST['price']
    #products[pk]['quantity'] += int(quantity)
    #products[key]['quantity'] = unicode(products[key]['quantity'],"utf-8")
    products[pk]= {'name':name,'size':size,'quantity':quantity,'price':price}
    request.session['cart'] = products
    return HttpResponseRedirect('/tkartapp/store/')

def viewcart(request,template_name='store/cart.html'):
    try:
        products = request.session['cart']
    except KeyError:
        return HttpResponseRedirect('/tkartapp/store/invalid_session/')
    for key in products.keys():
        shirt = Shirt.objects.all().get( id = key)
        products[key]['price'] = str(Decimal(products[key]['quantity']) * shirt.price)
        products[key]['price'] = unicode(products[key]['price'],"utf-8")
    request.session['order'] = products

    return render(request,template_name,{'products':products})

def checkout(request,template_name='store/checkout.html'):
    try:
        order = request.session['order']
    except KeyError:
        return HttpResponseRedirect('/tkartapp/store/invalid_session/')
    quantity = 0
    price = 0
    for key in order:
        shirt = Shirt.objects.get(id= key)
        if shirt.quantity < int(order[key]['quantity']):
            del request.session['cart']
            del request.session['order']
            return HttpResponseRedirect('/tkartapp/store/outofstock/')
        else:
            shirt.quantity -= int(order[key]['quantity'])
            shirt.save()
            quantity = Decimal(quantity)  + Decimal(order[key]['quantity'])
            price = Decimal(price) + Decimal(order[key]['price'])
            del request.session['cart']
            del request.session['order']
        return render(request,template_name,{'quantity':str(quantity),'price':str(price),})

def invalid_session(request):
    return render_to_response('store/invalid_session.html')

def outofstock(request):
    return render_to_response('store/outofstock.html')

def login(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('registration/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/tkartapp/loggedin/')
    else:
        return HttpResponseRedirect('/tkartapp/invalid/')

def loggedin(request):
    return render_to_response('registration/loggedin.html',{'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('registration/invalid_login.html')

def logout(request):
    auth.logout(request)

    return render_to_response('registration/logout.html')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/tkartapp/register_success/')
    else:
        form = RegistrationForm()
    data = RequestContext(request, {'form': form})

    return render_to_response('registration/register.html',data,)


def register_success(request):
    return render_to_response('registration/register_success.html')

