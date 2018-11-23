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
    fields = ['mes', 'ano']
    success_url = reverse_lazy('listaprestacao')


class atualizaprestacao(UpdateView):
    model = prestacao
    fields = ['mes', 'ano']
    success_url = reverse_lazy('listaprestacao')

    def get_context_data(self, *args, **kwargs):
        context = super(atualizaprestacao, self).get_context_data(*args, **kwargs)
        context['lancamentos'] = lancamentos.objects.filter(prestacao=self.object)
        context['prestacao'] = self.kwargs['pk']
        return context


class deleteprestacao(DeleteView):
    model = prestacao
    success_url = reverse_lazy('listaprestacao')


class crialancamento(CreateView):
    model = lancamentos
    fields = ['prestacao','descricao', 'valormoeda']
    #success_url = reverse_lazy('atualizaprestacao')

    def get_success_url(self):
        return reverse('atualizaprestacao', kwargs={'pk': self.kwargs['prestacao']})
    
    def get_initial(self):
        initial = super(crialancamento, self).get_initial()
        initial = initial.copy()
        initial['prestacao'] = prestacao.objects.get(pk=self.kwargs.get('prestacao', None))
        return initial