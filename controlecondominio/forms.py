from django import forms
from controlecondominio.models import *
from django.utils import timezone

class lancamentosforms(forms.ModelForm):
    class Meta:
        model = lancamentos
        fields = ['tipolancamento', 'data', 'descricao', 'valormoeda']
    data = forms.DateField(widget = forms.DateInput(attrs={'class':'datepicker','style': 'width:100px'}), help_text="Data do Pagamento", initial=timezone.now)