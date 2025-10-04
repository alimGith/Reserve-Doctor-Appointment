from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, DoctorRegistrationForm, DoctorEditForm
from .models import Doctor

# ویو ثبت‌نام کاربر
from .forms import UserRegistrationForm, DoctorRegistrationForm, DoctorProfileForm
from django.contrib.auth.decorators import login_required

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = User.objects.get(username = form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('login')
    else:
        messages.error(request, 'wrong input.')
        form = UserRegistrationForm()
    
    return render(request, 'users/register_user.html', {'form': form})

# ویو ثبت‌نام دکتر
def register_doctor(request):
    if request.method == 'POST':
        doctor_form = DoctorRegistrationForm(request.POST)
        profile_form = DoctorProfileForm(request.POST)
        if doctor_form.is_valid() and profile_form.is_valid():
            # cdu = user_form.cleaned_data
            # cdp = profile_form.cleaned_data
            # doc = User.objects.create_user(cdu['username'], cdu['first_name'], cdu['last_name'], cdu['email'], cdu['password'])
            # prof = User.objects.create_user(cdp['specialty'], cdp['phone_number'])
            # doc.save()
            # prof.save()
            user = doctor_form.save()
            user.set_password(doctor_form.cleaned_data['password'])  # Ensures password is hashed
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Doctor registered successfully.')
            return redirect('login')
    else:
        messages.error(request, 'wrong input.')
        doctor_form = DoctorRegistrationForm()
        profile_form = DoctorProfileForm()

    return render(request, 'users/register_doctor.html', {
        'doctor_form': doctor_form,
        'profile_form': profile_form
    })

# ویو لاگین کاربر
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # هدایت همه به داشبورد مشترک
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong username or password!')
            return render(request, 'users/login.html', {'error': 'نام کاربری یا رمز عبور اشتباه است.'})

    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    # چک کردن اینکه کاربر دکتر است یا خیر
    if hasattr(request.user, 'doctor'):
        #available_slots = request.user.doctor.available_slots.all()  # فرض بر این است که دکتر زمان‌های موجود دارد
        available_slots = request.user.doctor.available_slots.filter(is_booked=False)  # فرض بر این است که دکتر زمان‌های موجود دارد
        appointments = request.user.doctor.appointment_set.all()  # نمایش قرارها
        #appointments = Appointment.objects.filter(doctor=user.doctor)
        context = {
            'is_doctor': True,
            'available_slots': available_slots,
            'appointments': appointments,
        }
        return render(request, 'users/doctor_dashboard.html', context)
    else:
        # کاربر عادی
        appointments = request.user.appointment_set.all()
        #appointments = Appointment.objects.filter(patient=user)
        doctors = Doctor.objects.all()  # همه دکترها را برای انتخاب به قالب ارسال کنید  
        context = {
            'is_doctor': False,
            'appointments': appointments,
        }
        context['doctors'] = doctors
        return render(request, 'users/user_dashboard.html', context)
    #return render(request, 'users/dashboard.html', context)

# ویو خروج از حساب کاربری
def logout_user(request):
    logout(request)
    return redirect('login')  # بعد از خروج، به صفحه لاگین هدایت می‌شود

def index(request):
    # بررسی وجود کاربران و پزشکان
    if User.objects.exists() and Doctor.objects.exists():
        return redirect('login')  # هدایت به صفحه لاگین اگر کاربر وجود داشته باشد
    else:
        return redirect('register_doctor')  # هدایت به صفحه ثبت‌نام اگر کاربر وجود نداشته باشد

@login_required
def edit_profile(request):
    if hasattr(request.user, 'doctor'):
        doctor_form = DoctorEditForm(request.POST, instance=request.user)
        if request.method == 'POST' and doctor_form.is_valid():
            user = doctor_form.save()
            user.set_password(doctor_form.cleaned_data['password'])
            user.save()
            messages.success(request, 'changed successfully!')
            return redirect('login')
        return render(request, 'users/edit_profile.html', {'doctor_form': doctor_form})
    #return redirect('dashboard')
    