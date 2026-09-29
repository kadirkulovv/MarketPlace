from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            if user.role == 'seller':
                return redirect('dashboard:seller_dashboard')
            return redirect('products:home')
        else:
            messages.error(request, "Iltimos, shakldagi xatoliklarni tekshirib qayta urinib ko'ring.")
    else:
        role = request.GET.get('role', 'buyer')
        form = RegisterForm(initial={'role': role})

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.role == 'seller':
                return redirect('dashboard:seller_dashboard')
            return redirect('products:home')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('products:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi.")
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
