from django.db import models
from django.urls import reverse
from django.utils import timezone

ANOS = [
    (18, '2018'),
    (19, '2019'),
    (20, '2020'),
]

TIPOLANCAMENTO = [
    (1, 'Recebimento'),
    (0, 'Pagamento'),
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
    saldoanterior = models.DecimalField('Saldo Anterior', help_text="Saldo da prestacão anterior (R$)", default = 0 , max_digits=20, decimal_places=2 )

    class Meta:
        unique_together = ('ano', 'mes',)


    def get_absolute_url(self):
        return reverse('prestacao', kwargs={'id': self.pk})

    def __str__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())

    def __unicode__(self):
        return str(self.get_ano_display()) + " de " + str(self.get_mes_display())


class lancamentos(models.Model):
    tipolancamento = models.IntegerField('Tipo Lançamento', choices=TIPOLANCAMENTO, help_text="Tipo de lançamento", default=1)
    data = models.DateField('Data', help_text="Data do Pagamento", default=timezone.now)
    prestacao = models.ForeignKey('prestacao', verbose_name='prestacao', help_text="Prestação Ref.", on_delete=models.CASCADE)
    descricao = models.CharField('Descrição', help_text="Descrição do Lançamento", max_length=50,)
    valormoeda = models.DecimalField('Valor', help_text="Valor do lançamento (R$)", max_digits=20, decimal_places=2 )

    def get_absolute_url(self):
        return reverse('prestacao', kwargs={'id': self.pk})

    def __str__(self):
        return "Descrição: '" + str(self.descricao + "', valor: R$ " + str(self.valormoeda))
    
    def __unicode__(self):
        return str(self.descricao + " de " + str(self.valormoeda)) + " Reais"

    