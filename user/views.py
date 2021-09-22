from django.contrib.auth.forms import UsernameField
from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from user.forms import RegistrationForm


class RegistrationView(View):
    """ Register a new User """

    def get(self, request):
        """Render User Registration Page on GET request"""
        return render(request, 'user/register.html')

    def post(self, request):
        """Save the new User data to database on POST request"""
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'user/register.html', {'form': form, 'data': request.POST})


class CustomLoginView(LoginView):
    """Login User"""
    redirect_authenticated_user = 'index'
    def get(self, request):
        """Render Login page for user on GET request"""
        return render(request, 'user/login.html')

    def post(self, request, ):
        """Authenticate user on POST request"""
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_index')
            return redirect('index')
        else:
            return render(request, 'user/login.html', {'error':'Invalid Username or Password'})
        
    def get_success_url(self):
        return reverse_lazy('index')