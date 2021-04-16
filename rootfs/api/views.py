import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.views.generic.edit import CreateView
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.permissions import IsAuthenticated

from api import serializers
from api.exceptions import ServiceUnavailable
from api.serializers import RegisterForm
from api.utils import account_activation_token, get_local_host
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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            domain = get_local_host(request)
            mail_subject = 'Activate your account.'
            message = render_to_string(
                'registration/account_activation_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(mail_subject, message)
            messages.success(request, (
                'Please Confirm your email to complete registration.'))
            return redirect('login')
        else:
            return HttpResponse(form.errors, status=400)


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,
                                                                     token):  # noqa
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('/')
        else:
            messages.warning(request, (
                'The confirmation link was invalid, possibly because it has already been used.'))  # noqa
            return redirect('/')


def index(request):
    return render(request, 'index.html')


class UserDetailView(NormalUserViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user


class UserEmailView(NormalUserViewSet):
    serializer_class = serializers.UserEmailSerializer
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user
