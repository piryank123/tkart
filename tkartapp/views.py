import json
from collections import defaultdict
from decimal import Decimal

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core import serializers

from ipdb import set_trace

from .models import Shirt, UserProfile
from .forms import RegistrationForm, ShirtForm

@login_required(login_url='tkartapp:login')
def store(request,template_name = 'store/index.html'):
    shirts = Shirt.objects.all()
    cart = request.session.get('cart', {})
    for shirt in shirts:
        shirt.ordered_quantity = cart.get(str(shirt.id), 0)
    message = request.GET.get('message','')
    if message == 'error':
        message = 'You have selected an invalid quantity'

        return render(request,template_name,{'shirts': shirts,'message':message})
    elif message == 'done':
        message = 'Successfull Added to Cart'

        return render(request,template_name,{'shirts':shirts,'message':message})

    return render(request,template_name,{'shirts':shirts})

# @login_required(login_url='tkartapp:login')
# def shirt_list(request,template_name = 'store/admin.html'):
    # shirt = Shirt.objects.all
    # data  = {}
    # data['shirt_list_admin'] = shirt

    # return render(request,template_name,data)

# def shirt_create(request,template_name= 'store/form.html'):
    # form = ShirtForm(request.POST or None)
    # if form.is_valid():
        # form.save()
        # return redirect('tkartapp:shirt_list')

    # return render(request,template_name,{'form':form})

# def shirt_update(request,pk,template_name='store/form.html'):
    # shirt = get_object_or_404(Shirt, pk=pk)
    # form = ShirtForm(request.POST or None, instance = shirt)
    # if form.is_valid():
        # form.save()
        # return redirect('tkartapp:shirt_list')

    # return render(request,template_name,{'form':form})

# def shirt_delete(request, pk, template_name='store/delete.html'):
    # shirt= get_object_or_404(Shirt, pk=pk)
    # if request.method=='POST':
        # shirt.delete()
        # return redirect('tkartapp:shirt_list')

    # return render(request, template_name, {'object':shirt})

@login_required(login_url='tkartapp:login')
def add_to_cart(request):
    template_name='store/index.html'
    if request.method == 'POST':
        shirt_id = request.POST['id']
        quantity = int(request.POST['quantity'])
        if quantity < 1:

            return HttpResponseRedirect('/tkartapp/store/?message=error')
        else:
            cart = request.session.get('cart', {})
            shirt = Shirt.objects.filter(id=shirt_id).first()
            if shirt.quantity < quantity:

                return HttpResponseRedirect('/tkartapp/store/?message=error')
            else:
                cart[shirt_id]= quantity
                request.session['cart'] = cart

        return HttpResponseRedirect('/tkartapp/store/?message=done')

@login_required(login_url='tkartapp:login')
def viewcart(request,template_name='store/cart.html'):
    cart = request.session.get('cart', {})
    products = {}

    for shirt_id in cart:
        shirt = Shirt.objects.get(id=shirt_id)
        quantity_ordered = int(cart[shirt_id])
        products[shirt_id] = {
                'name': shirt.name,
                'size': shirt.size,
                'quantity':quantity_ordered,
                'price': quantity_ordered * shirt.price
                }

    return render(request,template_name,{'products':products})

@login_required(login_url='tkartapp:login')
def checkout(request,template_name='store/checkout.html'):
    cart = request.session.get('cart',{})
    quantity = 0
    price = 0
    for shirt_id in cart:
        shirt = Shirt.objects.get(id= shirt_id)
        shirt.quantity -= int(cart[shirt_id])
        shirt.save()
        quantity = Decimal(quantity)  + Decimal(cart[shirt_id])
        price = Decimal(price) + Decimal(shirt.price * cart[shirt_id])
    del request.session['cart']
    return render(request,template_name,{'quantity':str(quantity),'price':str(price),})

def invalid_session(request):
    return render_to_response('store/invalid_session.html')

# def outofstock(request):
    # return render_to_response('store/outofstock.html')

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

    return render_to_response('registration/register.html',data)

def register_success(request):
    return render_to_response('registration/register_success.html')

