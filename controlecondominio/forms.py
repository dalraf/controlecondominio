from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from controlecondominio.models import *

class lancamentos(forms.ModelForm):
    class Meta:
        model = lancamentos
        fields = ['data', 'descricao', 'valormoeda']
    data = forms.DateField(widget = forms.SelectDateWidget, help_text="Data do Pagamento")