from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.utils import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now

from gfg import settings
from .tokens import generate_token
from .models import Profile, Attendance, InternalMark

import json
import random
from collections import defaultdict
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404, redirect
from .models import InternalMark
from .forms import StudentMarkForm
from django.contrib.auth.decorators import login_required, user_passes_test


# Check if user is admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def edit_mark(request, mark_id):
    mark = get_object_or_404(StudentMark, id=mark_id)
    if request.method == 'POST':
        form = StudentMarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect('view_all_marks')  # or any other view
    else:
        form = StudentMarkForm(instance=mark)
    return render(request, 'edit_mark.html', {'form': form, 'mark': mark})


# Helper: safely get user's profile or redirect
def get_user_profile_or_redirect(request):
    try:
        return Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return None

# Views
def home(request):
    return render(request, "authentication/home.html")

def check_phno(request):
    phno = request.GET.get('phno')
    exists = Profile.objects.filter(phno=phno).exists()
    return JsonResponse({'exists': exists})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        rno = request.POST['rno']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address = request.POST['address']
        phno = request.POST['phno']
        gender = request.POST['gender']
        profile_image = request.FILES.get('profile_image') 

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists! Please try another username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered!")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters")

        if not username.isalnum():
            messages.error(request,"Username must be alphanumeric!")
            return redirect('home')
            
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return render(request, "authentication/signup.html")
        
        if Profile.objects.filter(phno=phno).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, "authentication/signup.html")

        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = True
            myuser.save()

            profile = Profile(user=myuser, rollno=rno, phno=phno, gender=gender, address=address, profile_image=profile_image)
            profile.save()

            messages.success(request, "Your account has been created successfully. We have sent you a confirmation email.")
            
            subject = "Welcome to GFG-Django Login!!!"
            message = f"Hello {myuser.first_name}!!\nWelcome to GFG!!!\nThank you for visiting our website.\nWe have sent you a confirmation email."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [myuser.email], fail_silently=True)

            current_site = get_current_site(request)
            email_subject = "Confirm your email @ gfg-django login!!"
            message2 = render_to_string('email_confirmation.html', {
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
            email.send(fail_silently=True)

            return redirect('/signin/')

        except IntegrityError:
            messages.error(request, "Error creating account. Try again.")
            return render(request, "authentication/signup.html")

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://{request.get_host()}/reset_password/{uid}/{token}/"
            message = render_to_string("password_reset_email.html", {
                'name': user.first_name,
                'reset_link': reset_link
            })
            EmailMessage("Reset Your Password", message, settings.EMAIL_HOST_USER, [email]).send()
            return HttpResponse("We have emailed you the password reset link.")
        else:
            return HttpResponse("No user found with this email.")

    return render(request, "authentication/forgot_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return HttpResponse("Password reset successfully. You can now <a href='/signin/'>login</a>.")
            else:
                return HttpResponse("Passwords do not match.")
        return render(request, "authentication/reset_password.html")
    else:
        return HttpResponse("Invalid or expired link.")

def dashboard(request):
    profile = get_user_profile_or_redirect(request)
    if profile is None:
        return redirect('home')

    records = Attendance.objects.filter(profile=profile)
    total_days = records.count() or 1

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        subject_totals = defaultdict(int)
        for record in records:
            for subject, value in record.attendance_summary().items():
                subject_totals[subject] += value
        subject_averages = {s: round(v / total_days, 2) for s, v in subject_totals.items()}
        return JsonResponse({'data': subject_averages})

    subject_totals = defaultdict(int)
    for record in records:
        for subject, value in record.attendance_summary().items():
            subject_totals[subject] += value
    subject_averages = {s: round(v / total_days, 2) for s, v in subject_totals.items()}

    return render(request, 'authentication/dashboard.html', {
        'profile': profile,
        'attendance_data': subject_averages
    })

def ordinal(n):
    return f"{n}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"

def internal_marks_view(request):
    profile = get_user_profile_or_redirect(request)
    if profile is None:
        return redirect('home')

    all_marks = InternalMark.objects.filter(profile=profile).order_by("semester")
    semester_wise = defaultdict(list)
    chart_json_data = {}

    for mark in all_marks:
        sem_key = ordinal(mark.semester)
        semester_wise[sem_key].append(mark)

    for sem_key, marks in semester_wise.items():
        labels, data, colors = [], [], []
        for m in marks:
            labels.append(m.subject)
            total = (m.theory_obtained_marks or 0) + (m.practical_obtained_marks or 0)
            data.append(total)
            colors.append(f"#{random.randint(0, 0xFFFFFF):06x}")
        chart_json_data[sem_key] = {"labels": labels, "data": data, "colors": colors}

    return render(request, "authentication/imarks.html", {
        "semester_wise": dict(semester_wise),
        "marks_json": json.dumps(chart_json_data),
    })

@staff_member_required
def admin_dashboard(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'authentication/admin_dashboard.html', {'profiles': profiles})

@staff_member_required
def view_marks(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    semesters = InternalMark.objects.filter(profile=profile).values_list('semester', flat=True).distinct()
    return render(request, 'authentication/view_marks.html', {'profile': profile, 'semesters': semesters})

@staff_member_required
def edit_marks(request, profile_id, semester):
    profile = get_object_or_404(Profile, id=profile_id)
    marks = InternalMark.objects.filter(profile=profile, semester=semester)

    if request.method == 'POST':
        for mark in marks:
            theory_key = f"theory_{mark.id}"
            practical_key = f"practical_{mark.id}"

            theory_value = request.POST.get(theory_key, "").strip()
            practical_value = request.POST.get(practical_key, "").strip()

            try:
                mark.theory_obtained_marks = Decimal(theory_value) if theory_value else None
            except (InvalidOperation, ValueError):
                mark.theory_obtained_marks = None

            try:
                mark.practical_obtained_marks = Decimal(practical_value) if practical_value else None
            except (InvalidOperation, ValueError):
                mark.practical_obtained_marks = None

            mark.save()

        messages.success(request, "Marks updated successfully.")
        return redirect('admin_dashboard')

    return render(request, 'authentication/edit_marks.html', {'profile': profile, 'marks': marks, 'semester': semester})

@staff_member_required
@login_required
def logged_in_users(request):
    users = User.objects.filter(last_login__isnull=False).order_by('-last_login')
    return render(request, 'authentication/logged_in_users.html', {'users': users})

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import StudentMark
from .forms import StudentMarkForm

@user_passes_test(lambda u: u.is_superuser)  # Only admins can edit marks
def edit_student_marks(request):
    marks = StudentMark.objects.all().order_by('student__username', 'subject')

    if request.method == 'POST':
        for mark in marks:
            form = StudentMarkForm(request.POST, instance=mark, prefix=str(mark.id))
            if form.is_valid():
                form.save()
        return redirect('edit_student_marks')  # Refresh page after saving

    forms_list = [(mark, StudentMarkForm(instance=mark, prefix=str(mark.id))) for mark in marks]
    return render(request, 'edit_marks.html', {'forms_list': forms_list})


