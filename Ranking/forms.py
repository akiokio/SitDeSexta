__author__ = 'GuilhermeAkio'
from django import forms
from django.core.mail import send_mail

class formContato(forms.Form):
    nome = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    mensagem = forms.Field(widget=forms.Textarea)

    def enviar(self):
        titulo = 'Mensagem enviada pelo site Sit De Sexta'
        destino = 'akio.xd@outlook.com'
        texto = """
        Nome: %(nome)s
        E-mail: %(email)s
        Mensagem:
        %(mensagem)s
        """ % self.cleaned_data

        send_mail(
            subject=titulo,
            message=texto,
            from_email=destino,
            recipient_list=[destino],
        )