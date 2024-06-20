from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views import View

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)
    
class UserLoginView(UserPassesTestMixin, LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("index")
    
    def test_func(self) -> bool | None:
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("index")
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))