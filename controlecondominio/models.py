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
    ano = models.IntegerField('Ano', choices=ANOS, default=1)
    mes = models.IntegerField('Mês', choices=MESES, default=18)

    def get_absolute_url(self):
        return reverse('prestacao', kwargs={'id': self.id})

    def __str__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())

    def __unicode__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())


class lancamentos(models.Model):
    prestacao = models.ForeignKey('prestacao', verbose_name='prestacao', on_delete=models.CASCADE)
    descricao = models.CharField('Descrição', max_length=50,)
    valormoeda = models.DecimalField('Valor', max_digits=4, decimal_places=2 )

    