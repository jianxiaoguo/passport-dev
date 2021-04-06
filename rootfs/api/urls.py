from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from django.contrib.auth import views as auth_views

from api import views
from api.views import RegisterView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'accounts/register/?$', RegisterView.as_view(template_name='register.html'), name='register'),
    url(r'accounts/login/?$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'accounts/logout/?$', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    url(r'accounts/password_change/?$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    url(r'accounts/password_change/done/?$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    url(r'accounts/password_reset/?$', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    url(r'accounts/password_reset/done/?$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'accounts/reset/<uidb64>/<token>/?$', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'accounts/reset/done/?$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


    url(r'accounts/', include('django.contrib.auth.urls')),

    url(r'oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    url(r'users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

]
