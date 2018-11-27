from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from controlecondominio.models import *
from controlecondominio.forms import *
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django import forms

from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html',)

@method_decorator(login_required, name='dispatch')
class listaprestacao(ListView):
    model = prestacao

@method_decorator(login_required, name='dispatch')
class criaprestacao(CreateView):
    model = prestacao
    fields = ['mes', 'ano']
    success_url = reverse_lazy('listaprestacao')

@method_decorator(login_required, name='dispatch')
class atualizaprestacao(UpdateView):
    model = prestacao
    fields = ['mes', 'ano']
    success_url = reverse_lazy('listaprestacao')

    def get_context_data(self, *args, **kwargs):
        context = super(atualizaprestacao, self).get_context_data(*args, **kwargs)
        context['lancamentosrecebimentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=1)
        context['lancamentospagamentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=0)
        context['somarecebimentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=1).aggregate(Sum('valormoeda'))['valormoeda__sum']
        context['somapagamentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=0).aggregate(Sum('valormoeda'))['valormoeda__sum']
        context['saldo'] = context['somarecebimentos'] - context['somapagamentos']
        context['prestacao'] = self.kwargs['pk']
        return context

@method_decorator(login_required, name='dispatch')
class deleteprestacao(DeleteView):
    model = prestacao
    success_url = reverse_lazy('listaprestacao')

@method_decorator(login_required, name='dispatch')
class crialancamento(CreateView):
    model = lancamentos
    form_class = lancamentosforms
    #fields = ['data', 'descricao', 'valormoeda']

    def get_context_data(self, *args, **kwargs):
        context = super(crialancamento, self).get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})

    def form_valid(self, form):
        form.instance.prestacao = prestacao.objects.get(pk=self.kwargs.get('prestacao', None))
        return super(crialancamento, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class atualizalancamento(UpdateView):
    model = lancamentos
    form_class = lancamentosforms
    #fields = ['data', 'descricao', 'valormoeda']

    def get_context_data(self, *args, **kwargs):
        context = super(atualizalancamento, self).get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})

@method_decorator(login_required, name='dispatch')
class deletelancamento(DeleteView):
    model = lancamentos
    success_url = reverse_lazy('listaprestacao')

    def get_context_data(self, *args, **kwargs):
        context = super(deletelancamento, self).get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})