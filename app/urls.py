
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('print', views.generate_pdf, name='print'),
    path('generate', views.generate, name='generate'),
    path('customers', views.customers, name='customers'),
    path('analy', views.analayis, name='analayis'),
    path('user', views.user, name='user'),
    path('requirments', views.orders, name='orders'),
    path('write', views.inker, name='inker'),
    
  




]
