from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from accounts.models import CustomUser, BuyerProfile, DealerProfile
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(View):
    """
    Handles user registration for buyers and dealers.
    """
    template_name = "register.html"

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")

            # Create profile based on role
            if role == "buyer":
                BuyerProfile.objects.create(user=user)
            elif role == "dealer":
                DealerProfile.objects.create(user=user)

            login(request, user)
            return redirect("home")  # Change to your home page URL name
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    """
    Handles user login.
    """
    template_name = "login.html"

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")  # Change to your home page URL name
            else:
                form.add_error(None, "Invalid username or password")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    """
    Logs out the current user.
    """
    login_url = reverse_lazy("login")

    def get(self, request):
        logout(request)
        return redirect("home")

