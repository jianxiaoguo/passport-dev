import logging

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.permissions import IsAuthenticated

from api import serializers
from api.exceptions import ServiceUnavailable
from api.viewset import NormalUserViewSet

logger = logging.getLogger(__name__)


class ReadinessCheckView(View):
    """
    Simple readiness check view to determine DB connection / query.
    """

    def get(self, request):
        try:
            import django.db
            with django.db.connection.cursor() as c:
                c.execute("SELECT 0")
        except django.db.Error as e:
            raise ServiceUnavailable("Database health check failed") from e

        return HttpResponse("OK")

    head = get


class LivenessCheckView(View):
    """
    Simple liveness check view to determine if the server
    is responding to HTTP requests.
    """

    def get(self, request):
        return HttpResponse("OK")

    head = get


from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ("username", "email")


class RegisterView(View):
    def post(self, request):
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
        else:
            form = RegisterForm()
        return render(request, 'register.html',
                      context={'form': form, 'next': redirect_to})


def index(request):
    return render(request, 'index.html')


class UserDetailView(NormalUserViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['profile']

    def get_object(self):
        return self.request.user


class UserEmailView(NormalUserViewSet):
    serializer_class = serializers.UserEmailSerializer
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['profile']

    def get_object(self):
        return self.request.user
