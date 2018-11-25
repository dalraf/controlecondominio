from django.db import models
from django.urls import reverse

# Create your models here.

ANOS = [
    (18, '2018'),
    (19, '2019'),
    (20, '2020'),
]

MESES = [
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
]


class prestacao(models.Model):
    ano = models.IntegerField('Ano', choices=ANOS, help_text="Ano ref.", default=1)
    mes = models.IntegerField('Mês', choices=MESES, help_text="Mês ref.", default=18)

    def get_absolute_url(self):
        return reverse('prestacao', kwargs={'id': self.pk})

    def __str__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())

    def __unicode__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())


class lancamentos(models.Model):
    prestacao = models.ForeignKey('prestacao', verbose_name='prestacao', help_text="Prestação Ref.", on_delete=models.CASCADE)
    descricao = models.CharField('Descrição', help_text="Descrição do Lançamento", max_length=50,)
    valormoeda = models.DecimalField('Valor', help_text="Valor do lançamento (R$)", max_digits=20, decimal_places=2 )

    def get_absolute_url(self):
        return reverse('prestacao', kwargs={'id': self.pk})

    def __str__(self):
        return "Descrição: '" + str(self.descricao + "', valor: R$ " + str(self.valormoeda))
    
    def __unicode__(self):
        return str(self.descricao + " de " + str(self.valormoeda)) + " Reais"

    