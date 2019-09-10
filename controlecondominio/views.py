from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from controlecondominio.models import lancamentos, prestacao
from controlecondominio.forms import lancamentosforms
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django import forms

from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
def index(request):
    return render(request, 'index.html',)

@method_decorator(login_required, name='dispatch')
class listaprestacao(ListView):
    model = prestacao

@method_decorator(login_required, name='dispatch')
class criaprestacao(PermissionRequiredMixin,CreateView):
    model = prestacao
    fields = ['mes', 'ano' , 'saldoanterior']
    success_url = reverse_lazy('listaprestacao')
    permission_required = ('prestacao.can_add' )

@method_decorator(login_required, name='dispatch')
class atualizaprestacao(PermissionRequiredMixin,UpdateView):
    model = prestacao
    fields = ['mes', 'ano', 'saldoanterior']
    permission_required = ('prestacao.can_change' )

    #success_url = reverse_lazy('listaprestacao')
    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['lancamentosrecebimentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=1)
        context['lancamentospagamentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=0)
        context['saldoanterior'] = prestacao.objects.filter(pk=self.kwargs['pk']).values_list('saldoanterior', flat=True)[0]
        context['somarecebimentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=1).aggregate(Sum('valormoeda'))['valormoeda__sum']
        context['somapagamentos'] = lancamentos.objects.filter(prestacao=self.object,tipolancamento=0).aggregate(Sum('valormoeda'))['valormoeda__sum']
        if context['somarecebimentos'] != None and context['somapagamentos'] != None:
            context['saldo'] = context['saldoanterior'] + context['somarecebimentos'] - context['somapagamentos']
        elif context['somarecebimentos'] != None:
            context['saldo'] = context['saldoanterior'] + context['somarecebimentos']
        elif context['somapagamentos'] != None:
            context['saldo'] = context['saldoanterior'] - context['somapagamentos']
        else:    
            context['saldo'] = context['saldoanterior']
        context['prestacao'] = self.kwargs['pk']
        return context

@method_decorator(login_required, name='dispatch')
class deleteprestacao(PermissionRequiredMixin,DeleteView):
    model = prestacao
    success_url = reverse_lazy('listaprestacao')
    permission_required = ('prestacao.can_delete' )

@method_decorator(login_required, name='dispatch')
class crialancamento(PermissionRequiredMixin,CreateView):
    model = lancamentos
    form_class = lancamentosforms
    permission_required = ('lancamentos.can_add' )
    #fields = ['data', 'descricao', 'valormoeda']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})

    def form_valid(self, form):
        form.instance.prestacao = prestacao.objects.get(pk=self.kwargs.get('prestacao', None))
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class atualizalancamento(PermissionRequiredMixin,UpdateView):
    model = lancamentos
    form_class = lancamentosforms
    permission_required = ('lancamentos.can_change' )
    #fields = ['data', 'descricao', 'valormoeda']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        context['lancamento'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})

@method_decorator(login_required, name='dispatch')
class deletelancamento(PermissionRequiredMixin,DeleteView):
    model = lancamentos
    success_url = reverse_lazy('listaprestacao')
    permission_required = ('lancamentos.can_delete' )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['prestacao'] = self.kwargs['prestacao']
        return context

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})