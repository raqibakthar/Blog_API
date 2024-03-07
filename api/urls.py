from django.urls import path
from account.views import RegisterView,LoginView
from home.views import BlogView,PubicView

urlpatterns = [
    
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),

    path('home/',BlogView.as_view()),
    path('public/',PubicView.as_view()),

]
