from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator

# @csrf_exempt
# def login_view(request):
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#
#     return render(request, 'registration/login.html')
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class CustomLoginView(LoginView):
#
#     template_name = 'registration/login.html'
#
#     def form_valid(self, form):
#         user: CustomUser = form.get_user()
#
#         login(self.request, user)
#
#         return redirect('index')