from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter


from api import views
from api.views import RegisterView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),

    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'accounts/register/?$', RegisterView.as_view(template_name='register.html'), name='register'),

    url(r'oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    url(r'users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

]
