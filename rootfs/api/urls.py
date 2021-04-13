from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter


from api import views
from api.views import RegisterView, ActivateAccount

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'accounts/', include('django.contrib.auth.urls')),

    url(r'accounts/register/?$', RegisterView.as_view(), name='register'),
    url(r'accounts/activate/<uidb64>/<token>/?$', ActivateAccount.as_view(), name='activate_account'),

    url(r'oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    url(r'users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

]
