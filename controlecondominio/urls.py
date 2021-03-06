from django.urls import path
from controlecondominio.views import atualizalancamento,atualizaprestacao, crialancamento, deletelancamento, deleteprestacao, listaprestacao, criaprestacao, index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('listaprestacao/', listaprestacao.as_view(template_name='listaprestacao.html'), name='listaprestacao'),
    path('prestacao/add/', criaprestacao.as_view(template_name='criaprestacao.html'), name='criaprestacao'),
    path('prestacao/edit/<int:pk>/', atualizaprestacao.as_view(template_name='atualizaprestacao.html'), name='atualizaprestacao'),
    path('prestacao/delete/<int:pk>/', deleteprestacao.as_view(template_name='deletaprestacao.html'), name='deletaprestacao'),
    path('lancamento/add/<int:prestacao>/', crialancamento.as_view(template_name='crialancamento.html'), name='crialancamento'),
    path('lancamento/edit/<int:prestacao>/<int:pk>/', atualizalancamento.as_view(template_name='atualizalancamento.html'), name='atualizalancamento'),
    path('lancamento/delete/<int:prestacao>/<int:pk>/', deletelancamento.as_view(template_name='deletalancamento.html'), name='deletalancamento'),
]