from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    
    return render(request, "users/profile.html", context)