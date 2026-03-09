from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'), 
    path('student/soft-delete/<int:pk>/', views.soft_delete_student, name='soft_delete_student'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('student/<int:student_id>/toggle_status/', views.toggle_status, name='toggle_status'),
    path('student/<int:id>/upload_documents/', views.upload_document, name='upload_document'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/created_at',views.created_at_view, name='created_at_view'),
    path('student/student_list', views.student_list, name='student_list'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path("dashboard/", views.dashboard, name="dashboard"),

]
