from django.urls import path
from . import views

urlpatterns = [
    #path('appointments/select-doctor/', views.view_available_slots, name='select_doctor'),
    path('appointments/select-doctor/<int:doctor_id>/', views.view_available_slots, name='select_doctor_with_id'),
    path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
    path('doctor/manage/', views.doctor_manage_appointments, name='doctor_manage_appointments'),
    path('add-slot/',views.add_available_slot, name = 'add-slot'),
    path('user-appointments', views.user_appointments, name = 'user_appointments'),
    path('upload-image/<int:patient_id>', views.image_upload_view, name='image_upload'),
    path('show-images/<int:patient_id>', views.image_list_view, name='image_list'),
    path('select_patient/', views.select_from_available_patients, name = 'select_patient'),
    path('select-patient-presc/', views.select_from_available_patients_presc, name = 'select_patient_presc'),
    path('prescription-list/<int:patient_id>', views.prescription_list_view, name = 'prescription_list'),
    path('prescription-write/<int:patient_id>', views.prescription_write_view, name = 'prescription_write'),
]