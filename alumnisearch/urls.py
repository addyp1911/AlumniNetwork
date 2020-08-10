from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf.urls import url

r_uuid = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('signup/', views.UserSignUp.as_view(), name='register'),
    path('login/', views.UserSignIn.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'),name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('alumni-list/', views.ListAlumni.as_view(), name='alumni-list'),
    url(r'^profile-show/(?P<id>%s)$' % r_uuid ,views.ProfileRetrieve.as_view(), name='profile-show')

]