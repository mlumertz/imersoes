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
from django.forms import formset_factory
from django.views.generic.edit import UpdateView
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from io import BytesIO

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

@login_required
def mudar_senha_view(request):
    
    template = loader.get_template('MudarSenha.html')
    context = {
        'user' : request.user
    }
    return render(request, 'MudarSenha.html' , context)


@login_required
def auth_mudar_senha_view(request):


    password = request.POST.get('password', '')
    NewPassword = request.POST.get('NewPassword', '')
    NewPassword2 = request.POST.get('NewPassword2', '')
    #user = auth.authenticate(username=username, password=password)

    CheckUser = auth.authenticate(username=request.user.username, password=password)
    if CheckUser is not None:
        if (NewPassword == NewPassword2):
            request.user.set_password(NewPassword)
            return HttpResponseRedirect('/Psicologo')    

    messages = "Senha invalida, tente novamente"
    context = {
    'message' : messages
    }
    return render(request, 'MudarSenha.html' , context)


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

   
    return HttpResponse(template.render(context, request))


@login_required
def novo_cliente_view(request):
        if request.method == 'POST':
            form = ClienteForm(request.user, request.POST)
            if form.is_valid():
                cliente = form.save()
                email = EmailMessage('Seu psicologo ' + request.user.username + ' iniciou um processo de feedback com você!' ,  'mlumertz.pythonanywhere.com/Cliente/' + str(cliente.WebKey) ,settings.EMAIL_HOST_USER, [cliente.Email])
                render_to_response('sucesso.html')
                email.send()
                ct1 = Categoria(cat = "Amigos", cliente = cliente)
                ct1.save()
                ct2 = Categoria(cat = "Familia", cliente = cliente)
                ct2.save()    
                return HttpResponseRedirect('/Psicologo')
                



        args = {}
        args.update(csrf(request))
        args['form'] = ClienteForm(request.user)
        return render_to_response('novo_cliente.html', args)


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


#def cliente_view(request, WebKey):

#    # Create the formset, specifying the form and formset we want to use.
#    cliente = Cliente.objects.get(WebKey=WebKey)
    
#    # lista = Indicado.objects.filter(QuemIndicou=cliente)

#    IndicadoFormSet = inlineformset_factory(Cliente, Categoria, Indicado, IndicadoForm )
   
# #if lista.count() > 0:
#    #    IndicadoFormSet = inlineformset_factory(Cliente, Indicado, fields=('Nome', 'Email'), formset=BaseIndicadoFormSet)
#    #else:
#    #    IndicadoFormSet = inlineformset_factory(Cliente, Indicado, fields=('Nome', 'Email'), formset=BaseIndicadoFormSet)

#    if request.method == 'POST':

#        cat_form = CategoriaForm();

#        if cat_form.is_valid():
#            categoria = cat_form.save(commit = False)
#            indicado_formset = IndicadoFormSet(request.POST, instance=categoria)
#            if  indicado_formset.is_valid():
#                categoria.save()
#                indicado_formset.save()
#                #newlista = Indicado.objects.filter(QuemIndicou=cliente)           
#                # for indicado in newlista:
#                    #email = EmailMessage('Seu amigo ' + indicado.Nome + ' indicou você!' , 'mlumertz.pythonanywhere.com/Indicado/' + str(indicado.WebKey) ,settings.EMAIL_HOST_USER, ['gabi.favieiro@gmail.com'])
#                    #email.send()
                
#                return render_to_response('sucesso.html')

           
#    else:
#        cat_form = CategoriaForm();
#        indicado_formset = IndicadoFormSet(instance=Categoria())

#    context = {
#        'cat_form': cat_form,
#        'formset': indicado_formset,
#        'cliente' : cliente,
#        }

#    return render(request, 'cliente.html', context)




#def cliente_view(request, WebKey):

#    # Create the formset, specifying the form and formset we want to use.
#    cliente = Cliente.objects.get(WebKey=WebKey)
#    lista = Indicado.objects.filter(QuemIndicou=cliente)

#    IndicadoFormSet = inlineformset_factory(Cliente, Indicado, fields=('Nome', 'Email'), formset=BaseIndicadoFormSet)

#    if request.method == 'POST':
#        formset = IndicadoFormSet(request.POST, instance=cliente)

#        if  formset.is_valid():
#            formset.save()
#            newlista = Indicado.objects.filter(QuemIndicou=cliente)
            
#            for indicado in newlista:
#                #email = EmailMessage('Seu amigo ' + indicado.Nome + ' indicou você!' , 'mlumertz.pythonanywhere.com/Indicado/' + str(indicado.WebKey) ,settings.EMAIL_HOST_USER, ['gabi.favieiro@gmail.com'])
#                #email.send()
#                return render_to_response('sucesso.html')


#    else:
#        formset = IndicadoFormSet(instance=cliente)

#    context = {
#        'formset': formset,
#        'cliente' : cliente
#    }

#    return render(request, 'cliente.html', context)

def cadastro_indicados_view(request, WebKey):

    cliente = Cliente.objects.get(WebKey=WebKey)
    cliente_formsetFactory = inlineformset_factory(Cliente, Indicado, form = IndicadoForm(cliente= cliente), extra = 1)
    
    listCat = Categoria.objects.filter(cliente=cliente)

   
    if request.method == 'POST':
        formset = cliente_formsetFactory(request.POST, instance=cliente)
        if formset.is_valid():
            indicados = formset.save()
            path = '/Cliente/%s' % WebKey
            return  HttpResponseRedirect(path)

    formset = cliente_formsetFactory(instance=cliente)
    context = {
        'formset': formset,
        'cliente' : cliente,
        'listCat' : listCat
        }

    return render(request, 'cadastro_indicados.html', context)


def cliente_view(request, WebKey):
    
    cliente = Cliente.objects.get(WebKey=WebKey)
 
    Nested_formset = nested_formset_factory(
            Cliente,
            Categoria,
            Indicado,
            CategoriaForm,
            IndicadoForm,
            extra =1)

    if request.method == 'POST':

        formset = Nested_formset(request.POST, instance=cliente)

        if formset.is_valid():
            indicados = formset.save()
            return render_to_response('sucesso.html')
    else:
        formset = Nested_formset(instance=cliente)

    context = {
        'categorias': formset,
        'cliente' : cliente,
        }

    return render(request, 'cliente.html', context)





def create_report(request, WebKey):

    cliente = Cliente.objects.get(WebKey=WebKey)
    pdfName = "report_%s.pdf" % cliente.Nome

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'  % pdfName

    buff = BytesIO()
    # Create the PDF object, using the response object as its "file."
  

    menu_pdf = SimpleDocTemplate(buff, pagesize=letter, rightMargin=72,
                                leftMargin=72, topMargin=40, bottomMargin=18)

    logo = "./Feedbacks/static/images/logo.png"
    im = Image(logo, 2*cm, 2*cm, hAlign = 'RIGHT')

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='justify', alignment=TA_JUSTIFY))

    # container for pdf elements
    elements = []


    elements.append(im);
    elements.append(Paragraph("Relatório de Respostas Compiladas", styles["Title"] ))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("Orientador: %s" %  cliente.Orientador.username , styles["Normal"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Cliente: %s" % cliente.Nome, styles["Normal"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Tipo de Feedback: %s" % cliente.TipoDeFeedback, styles["Normal"]))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("Pergunta 01:", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", styles["Definition"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Pergunta 02: ", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", styles["Definition"]))


    menu_pdf.build(elements)
    response.write(buff.getvalue())
    buff.close()
    return response