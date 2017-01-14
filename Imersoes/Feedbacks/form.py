from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import BaseInlineFormSet
from datetime import datetime
from Feedbacks.models import *


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nome', 'Email', 'TipoDeFeedback']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ClienteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        cliente = super(ClienteForm, self).save(commit = False)
        cliente.Orientador = self.user

        if commit:
            cliente.save()
        return cliente

class IndicadoForm(ModelForm):

    class Meta:
        model = Indicado
        fields = ['Nome', 'Email']


class BaseIndicadoFormSet(BaseInlineFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        nomes = []
        emails = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                nome = form.cleaned_data['Nome']
                email = form.cleaned_data['Email']

                # Check that no two links have the same anchor or URL
                if nome and email:
                    if nome in nomes:
                        duplicates = True
                    nomes.append(nome)

                    if email in emails:
                        duplicates = True
                    emails.append(nome)

                if duplicates:
                    raise forms.ValidationError(
                        'Indicados devem ter nome e email único',
                        code='indicados_duplicados'
                    )

                # Check that all links have both an anchor and URL
                if email and not nome:
                    raise forms.ValidationError(
                        'Todos os indicados devem ter um nome associado.',
                        code='missing_nome'
                    )
                elif nome and not email:
                    raise forms.ValidationError(
                        'Todos os indicados devem ter um email associado.',
                        code='missing_email'
                    )