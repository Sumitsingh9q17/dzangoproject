from django.urls import path
from authorization import views

urlpatterns = [
   path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountview.as_view(), name='activate'),
]
