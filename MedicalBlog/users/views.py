from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from users.forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, PasswordUpdateForm


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Replace with your login URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Replace 'home' with your desired URL name
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordUpdateForm(request.POST)

        if 'update_info' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Your account details have been updated.")
                return redirect('profile')

        elif 'update_password' in request.POST:
            if password_form.is_valid():
                current_password = password_form.cleaned_data.get('current_password')
                new_password = password_form.cleaned_data.get('new_password')
                if request.user.check_password(current_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Prevent logout after password change
                    messages.success(request, "Your password has been updated.")
                    return redirect('index')
                else:
                    password_form.add_error('current_password', "Incorrect current password.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordUpdateForm()

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'update_user.html', context)