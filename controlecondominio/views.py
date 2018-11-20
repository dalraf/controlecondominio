from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from controlecondominio.models import *

from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html',)


class listaprestacao(ListView):
    model = prestacao

class criaprestacao(CreateView):
    model = prestacao
    fields = ['mes','ano']
    success_url = reverse_lazy('listaprestacao')

class atualizaprestacao(UpdateView):
    model = prestacao
    fields = ['mes','ano']
    success_url = reverse_lazy('listaprestacao')

class deleteprestacao(DeleteView):
    model = prestacao
    success_url = reverse_lazy('listaprestacao')