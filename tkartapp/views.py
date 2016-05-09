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

def addtocart(request,pk,template_name='store/cart.html'):
    shirt = Shirt.objects.filter(id = pk).values()
    data  ={}
    data['cart'] = shirt

    return render(request,template_name,data)

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
        return HttpResponseRedirect('tkartapp:loggedin')
    else:
        return HttpResponseRedirect('tkartapp:invalid')

def loggedin(request):
    return render_to_response('registration/loggedin.html',
                              {'full_name': request.user.username})

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
            return HttpResponseRedirect('tkartapp:register_success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html',variables,)


def register_success(request):
    return render_to_response('registration/register_success.html')

