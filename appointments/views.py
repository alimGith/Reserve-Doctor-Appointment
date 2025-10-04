from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm, AvailableSlotForm, ImageUploadForm, PrescreptionModelForm
from .models import Appointment, AvailableSlot, ImageModel, Prescreption_Model
from users.models import Doctor
from django.contrib import messages
from users.models import Doctor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def select_from_available_patients_presc(request):    
   # دریافت شی دکتر از مدل Doctor بر اساس کاربر لاگین شده
    doctor = get_object_or_404(Doctor, user=request.user)

    # دریافت بیمارانی که برای این دکتر وقت گرفته‌اند
    appointments = Appointment.objects.filter(doctor=doctor)
    patients = [appointment.patient for appointment in appointments]

    if request.method == 'POST':
        # دریافت ID بیمار از فرم
        patient_id = request.POST.get('patient_id')
        print('user id : ', patient_id) #denug  ###################
        patient = get_object_or_404(User, id=patient_id)
        action = request.POST.get('action')

        if action == "give_prescription" :
            return redirect('prescription_write', patient_id=patient.id)
        elif action == "show_prescription" :
            return redirect('prescription_list', patient_id=patient.id)

    return render(request, 'appointments/show_patients_presc.html', {'patients': patients})

@login_required
def prescription_write_view(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    
    if request.method == 'POST':
        form = PrescreptionModelForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.uploaded_by = request.user  # دکتری که تصویر را آپلود می‌کند
            prescription.title = form.cleaned_data['title']  # مقدار title را از فرم دریافت می‌کنیم
            prescription.text = form.cleaned_data['text']
            prescription.save()
            messages.success(request, 'prescription has been successfully uploaded')
            return redirect('prescription_list', patient_id=patient.id)
    else:
        form = PrescreptionModelForm()

    return render(request, 'users/prescription_write.html', {'form': form, 'patient': patient})

@login_required
def prescription_list_view(request, patient_id):
    if hasattr(request.user, 'doctor'):
        #doctor = request.user.doctor
        doctor = Doctor.objects.get(user=request.user)
        
        if patient_id:
            # یافتن بیمار با استفاده از patient_id
            patient = get_object_or_404(User, id=patient_id)

        # چک کردن اینکه این دکتر توسط این بیمار رزرو شده باشد
        if Appointment.objects.filter(doctor=doctor, patient=patient).exists():
            prescriptions = Prescreption_Model.objects.filter(patient=patient)
        else:
            prescriptions = None
            messages.error(request, 'no appointments with this patient is set') 
        context = {'prescriptions': prescriptions, 'patient': patient, 'is_doctor' : True, 'specialty' : doctor.specialty}
    else:        
        if patient_id:
            # یافتن بیمار با استفاده از patient_id
            patient = get_object_or_404(User, id=patient_id)
            username = patient.username
        else:
            print('no patient_id found') #debug
        # چک کردن اینکه این دکتر توسط این بیمار رزرو شده باشد
        if Appointment.objects.filter(patient=patient).exists():
            prescriptions = Prescreption_Model.objects.filter(patient=patient)
        else:
            prescriptions = None
            messages.error(request, 'no appointments with this patient is set')
        context = {'prescriptions': prescriptions, 'patient': patient, 'is_doctor' : False}
    return render(request, 'users/prescription_list.html', context=context)
# @login_required
# def select_from_available_patients(request):
#     doctor = request.user.doctor
#     appointments = Appointment.objects.filter(doctor = doctor,)
#     #patients = appointments.patient.all()#wrong _ appointments is a QuerySet and has no attribute patient
#     patients = appointments.values_list('patient', flat=True)  # برگرداندن فقط فیلد patient
#     return render(request, 'appointments/show_patients.html', context={'patients' : patients})
@login_required
def select_from_available_patients(request):    
   # دریافت شی دکتر از مدل Doctor بر اساس کاربر لاگین شده
    doctor = get_object_or_404(Doctor, user=request.user)

    # دریافت بیمارانی که برای این دکتر وقت گرفته‌اند
    appointments = Appointment.objects.filter(doctor=doctor)
    patients = [appointment.patient for appointment in appointments]

    if request.method == 'POST':
        # دریافت ID بیمار از فرم
        patient_id = request.POST.get('patient_id')
        print('user id : ', patient_id) #denug  ###################
        patient = get_object_or_404(User, id=patient_id)
        action = request.POST.get('action')

        if action == 'upload':
            return redirect('image_upload', patient_id=patient.id)
        elif action == 'show_images':
            return redirect('image_list', patient_id=patient.id)
        elif action == "give_prescription" :
            return redirect('prescription_write', patient_id=patient.id)
        elif action == "show_prescription" :
            return redirect('prescription_list', patient_id=patient.id)

    return render(request, 'appointments/show_patients.html', {'patients': patients})

# @login_required
# def image_upload_view(request):
#     doctor = request.user.doctor
#     if request.method == 'POST':                
#         form = ImageUploadForm(request.POST, request.FILES)  # گرفتن داده‌ها و فایل‌ها از فرم
#         if form.is_valid():
#             form.save()
#             return redirect('image_list')  # پس از ذخیره به لیست تصاویر هدایت می‌شود
#     else:
#         form = ImageUploadForm()
#     return render(request, 'users/upload_image.html', {'form': form, 'doctor' : doctor})

@login_required
def image_upload_view(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.patient = patient
            image.uploaded_by = request.user  # دکتری که تصویر را آپلود می‌کند
            image.title = form.cleaned_data['title']  # مقدار title را از فرم دریافت می‌کنیم
            image.save()
            messages.success(request, 'image has been successfully uploaded')
            return redirect('image_upload', patient_id=patient.id)
    else:
        form = ImageUploadForm()

    return render(request, 'users/upload_image.html', {'form': form, 'patient': patient})

# @login_required
# def image_list_view(request):
#     images = ImageUpload.objects.all()  # گرفتن تمام عکس‌ها از دیتابیس
#     return render(request, 'users/show_image.html', {'images': images})

def image_list_view(request, patient_id=None):
    if hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        
        if patient_id:
            # یافتن بیمار با استفاده از patient_id
            patient = get_object_or_404(User, id=patient_id)
        # elif request.method == 'GET':
        #     # دریافت یوزرنیم بیمار از فرم
        #     username = request.GET.get('username')
        #     patient = get_object_or_404(User, username=username)            
        
        # چک کردن اینکه این دکتر توسط این بیمار رزرو شده باشد
        if Appointment.objects.filter(doctor=doctor, patient=patient).exists():
            images = ImageModel.objects.filter(patient=patient)
        else:
            images = None
            messages.error(request, 'no appointments with this patient is set') 
        context = {'images': images, 'patient': patient, 'is_doctor' : True}
    else:
        print('########################patient --> see images ? ') # debug
        if patient_id:
            # یافتن بیمار با استفاده از patient_id
            patient = get_object_or_404(User, id=patient_id)
            username = patient.username
        else:
            print('no patient_id found') #debug
        # چک کردن اینکه این دکتر توسط این بیمار رزرو شده باشد
        if Appointment.objects.filter(patient=patient).exists():
            images = ImageModel.objects.filter(patient=patient)
        else:
            images = None
            messages.error(request, 'no appointments with this patient is set')
        context = {'images': images, 'patient': patient, 'is_doctor' : False}
    return render(request, 'users/show_image.html', context=context)
    
@login_required
def view_available_slots(request, doctor_id=None):
    #if request.method == 'POST':
    #doctor_id = request.POST.get('doctor_id')
    if doctor_id:
        # نمایش زمان‌های خالی برای دکتر انتخاب‌شده
        doctor = get_object_or_404(Doctor, id=doctor_id)
        #available_slots = doctor.available_slots.all()
        available_slots = doctor.available_slots.filter(is_booked=False).order_by('start_time')
        return render(request, 'appointments/available_slots.html', {'available_slots': available_slots, 'doctor': doctor})
    else:
        # نمایش لیست دکترها برای انتخاب
        doctors = Doctor.objects.all()
        return render(request, 'users/user_dashboard.html', {'doctors': doctors})
    return HttpResponse("Invalid request", status=400)#debug
@login_required
def book_appointment(request, slot_id):##################################################
    print("####debug : Booking view called with slot_id:", slot_id)  # Debugging line
    slot = get_object_or_404(AvailableSlot, id=slot_id)
    #if Appointment.objects.filter(available_slot=slot, , doctor_id=slot.doctor.id).exists():    
    if Appointment.objects.filter(available_slot=slot).exists():    
    #if Appointment.objects.filter(available_slot=slot, available_slot__start_time=slot.start_time).exists():
        print("####debug : Appointment already exists")  # Debugging line
        messages.error(request, 'This slot is already booked!')
        doctor_id = slot.doctor.id
        #return redirect(f'select_doctor/{doctor_id}') ##################################################
        return redirect('select_doctor_with_id', doctor_id=doctor_id)
        

    if request.method == 'POST':
        print("####debug : POST request received")  # Debugging line
        print('####debug : slot.start_time : ', slot.start_time)

        # # کپی داده‌های POST برای تغییر
        # post_data = request.POST.copy()
        # # اضافه کردن appointment_time از slot.start_time به داده‌های POST
        # post_data['appointment_time'] = slot.start_time

    #     form = AppointmentForm(request.POST)
    #     if form.is_valid():
    #         print("####debug : Form is valid")  # Debugging line
    #         appointment = form.save(commit=False)
    #         appointment.available_slot = slot
    #         appointment.patient = request.user
    #         appointment.appointment_time = slot.start_time  # Using the slot's start time
    #         appointment.save()
    #         messages.success(request, 'Appointment booked successfully!')
    #         return redirect('user_appointments')
    #     else:
    #         print("####debug : Form is invalid")
    #         print(form.errors)  # نمایش خطاهای فرم
    # else:
    #     print("####debug : Request is not POST")  # Debugging line
    #     form = AppointmentForm()
        appointment = Appointment(
            available_slot=slot,
            patient=request.user,
            appointment_time=slot.start_time,
            doctor=slot.doctor  # اضافه کردن دکتر از اسلات
        )        
        appointment.save()
        # بروزرسانی وضعیت رزرو اسلات
        slot.is_booked = True
        slot.save()
        messages.success(request, 'Appointment booked successfully!')
        return redirect('dashboard')

    return redirect('select_doctor_with_id', doctor_id=slot.doctor.id)

# @login_required
# def add_available_slot(request):
#     if request.method == 'POST':
#         form = AvailableSlotForm(request.POST)
#         if form.is_valid():
#             slot = form.save(commit=False)
#             slot.doctor = request.user.doctor  # پزشک وارد شده به سیستم
#             slot.save()
#             return redirect('dashboard')
#     else:
#         form = AvailableSlotForm()
#     return render(request, 'appointments/add_slot.html', {'form': form})



# @login_required
# def add_available_slot(request):
#     if request.method == 'POST':
#         form = AvailableSlotForm(request.POST)
#         if form.is_valid():
#             slot = form.save(commit=False)
#             slot.doctor = request.user.doctor
#             slot.save()
#             messages.success(request, 'Slot added successfully!')
#             return redirect('/users/dashboard')
#     else:
#         form = AvailableSlotForm()

#     return render(request, 'appointments/add_slot.html', {'form': form})
@login_required
def add_available_slot(request):
    if request.method == 'POST':
        form = AvailableSlotForm(request.POST)
        if form.is_valid():
            # داده‌های فرم را دریافت کن
            doctor = request.user.doctor
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
                        
            # بررسی اینکه آیا Slot تکراری است
            existing_slot = AvailableSlot.objects.filter(doctor=doctor, start_time=start_time).exists()
            if existing_slot:
                messages.error(request, 'A slot with the same start time already exists for this doctor.')
                return render(request, 'appointments/add_slot.html', {'form': form})
            
            # بررسی هم‌پوشانی زمانی
            overlapping_slot = AvailableSlot.objects.filter(doctor=doctor).filter(
                start_time__lt=end_time, end_time__gt=start_time
            ).exists()

            if overlapping_slot:
                messages.error(request, 'This slot overlaps with an existing slot for this doctor.')
                return render(request, 'appointments/add_slot.html', {'form': form})

            # اگر تکراری یا تداخل نبود، Slot را ذخیره کن
            slot = form.save(commit=False)
            slot.doctor = request.user.doctor
            slot.save()
            messages.success(request, 'Slot added successfully!')
            return redirect('/users/dashboard')
        
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AvailableSlotForm()

    return render(request, 'appointments/add_slot.html', {'form': form})

@login_required
def doctor_manage_appointments(request): ##################################################
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor)
    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/doctor_appointments.html', context)

def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor__user=request.user)
    return render(request, 'users/doctor_appointments.html', {'appointments': appointments})

def user_appointments(request):
    #appointments = Appointment.objects.filter(patient=request.user)
    appointments = Appointment.objects.filter(patient=request.user).order_by('start_time')
    return render(request, 'users/user_appointments.html', {'appointments': appointments})


