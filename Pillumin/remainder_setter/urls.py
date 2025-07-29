from django.urls import path

from . import views

urlpatterns=[
    path('reminder/', views.set_reminder, name='set_remainder')  # 🔁 fix here


]
