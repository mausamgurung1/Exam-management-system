from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    # Public routes
    path('edit-marks/', views.edit_student_marks, name='edit_student_marks'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('check-phno/', views.check_phno, name='check_phno'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    # Email verification and password reset
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    # Student dashboard and marks view
    path("dashboard/", views.dashboard, name="dashboard"),
    path("internal_marks_view/", views.internal_marks_view, name="internal_marks_view"),

    # Admin routes
    path('admin-login/', auth_views.LoginView.as_view(template_name='authentication/admin_login.html'), name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-view-marks/<int:profile_id>/', views.view_marks, name='view_marks'),
    path('admin-edit-marks/<int:profile_id>/<int:semester>/', views.edit_marks, name='edit_marks'),
    path('edit_mark/<int:mark_id>/', views.edit_mark, name='edit_mark'),


    # Optional: View list of users who have logged in
    path('logged-in-users/', views.logged_in_users, name='logged_in_users'),
]

# Development static + media files handling
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
