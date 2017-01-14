from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import loader
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import *  
from .form import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.forms import inlineformset_factory

# Create your views here.

def login(request):

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/Psicologo')

    c = {}
    c.update(csrf(request))
    return render_to_response('login.html' ,c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/Psicologo')
    
    else:
        return HttpResponseRedirect('/invalid')

def loggedin(request):
    return render_to_response('loggedin.html', 
                             {'full_name' : request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def Psicologo_view(request):
    template = loader.get_template('Psicologo.html')
    context = {
        'user' : request.user,
        'clientes' : Cliente.objects.filter(Orientador = request.user)
    }
    testecliente = Cliente.objects.filter(Orientador = request.user)
    user = request.user

    return HttpResponse(template.render(context,request))

@login_required
def novo_cliente_view(request):
        if request.method == 'POST':
            form = ClienteForm(request.user, request.POST)
            if form.is_valid():
                cliente = form.save()
                email = EmailMessage('Seu psicologo ' + request.user.username + ' iniciou um processo de feedback com você!' , str(cliente.WebKey) ,settings.EMAIL_HOST_USER, ['gabi.favieiro@gmail.com'])
                email.send()
                return HttpResponseRedirect('/Psicologo')

        args = {}
        args.update(csrf(request))
        args['form'] = ClienteForm(request.user)
        return render_to_response('novo_cliente.html', args)


def cliente_view(request, WebKey):

    # Create the formset, specifying the form and formset we want to use.
    cliente = Cliente.objects.get(WebKey=WebKey)
    lista = Indicado.objects.filter(QuemIndicou=cliente)

    if lista.count() > 0:
        IndicadoFormSet = inlineformset_factory(Cliente, Indicado, fields=('Nome', 'Email')) #, formset=BaseIndicadoFormSet)
    else:
        IndicadoFormSet = inlineformset_factory(Cliente, Indicado, fields=('Nome', 'Email')) #, formset=BaseIndicadoFormSet)

    if request.method == 'POST':
        formset = IndicadoFormSet(request.POST, instance=cliente)

        if  formset.is_valid():
            formset.save()
            newlista = Indicado.objects.filter(QuemIndicou=cliente)
            
            for indicado in newlista:
                email = EmailMessage('Seu amigo ' + indicado.Nome + ' indicou você!' , str(indicado.WebKey) ,settings.EMAIL_HOST_USER, ['gabi.favieiro@gmail.com'])
                email.send()

            return render_to_response('sucesso.html')


    else:
        formset = IndicadoFormSet(instance=cliente)

    context = {
        'formset': formset,
        'cliente' : cliente
    }

    return render(request, 'cliente.html', context)


def sucesso(request):
    return render_to_response('sucesso.html')

def indicado_view(request, WebKey):

    indicado = Indicado.objects.get(WebKey=WebKey)

    if request.method == 'POST':
        form = IndicadoPageForm(request.POST, instance = indicado)

        if  form.is_valid():
            form.save()
            return render_to_response('sucesso.html')


    else:
        args = {}
        args.update(csrf(request))
        args['form'] = IndicadoPageForm( instance = indicado)

        return render_to_response( 'indicado.html', args)