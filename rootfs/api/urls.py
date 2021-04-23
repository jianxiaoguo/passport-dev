from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter


from api import views
from api.views import RegisterView, ActivateAccount, RegisterDoneView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^', include(router.urls)),
    re_path(r'accounts/', include('django.contrib.auth.urls')),

    re_path(r'accounts/register/?$', RegisterView.as_view(), name='register'),
    re_path(r'accounts/activate/<uidb64>/<token>/?$', ActivateAccount.as_view(), name='activate_account'),
    re_path(r'accounts/register/done/?$', RegisterDoneView.as_view(), name='register_done'),

    re_path(r'oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    re_path(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    re_path(r'users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

]
