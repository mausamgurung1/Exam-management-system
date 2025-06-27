from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

class StudentMark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    full_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollno = models.CharField(max_length=20, unique=True)  # Making rollno unique
    phno = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")],
        unique=True
    )
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  


    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    engineering_economics = models.IntegerField(default=0)
    algorithm_analysis_and_design = models.IntegerField(default=0)
    numerical_method = models.IntegerField(default=0)
    research_methodology = models.IntegerField(default=0)
    computer_architecture_and_design = models.IntegerField(default=0)
    operating_system = models.IntegerField(default=0)

    def attendance_summary(self):
        return {
            "Engineering Economics": self.engineering_economics,
            "Algorithm Analysis and Design": self.algorithm_analysis_and_design,
            "Numerical Method": self.numerical_method,
            "Research Methodology": self.research_methodology,
            "Computer Architecture and Design": self.computer_architecture_and_design,
            "Operating System": self.operating_system,
        }
    
class InternalMark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    semester = models.IntegerField()
    subject = models.CharField(max_length=100)

    # Theory marks
    theory_full_marks = models.PositiveIntegerField(default=0)
    theory_pass_marks = models.PositiveIntegerField(default=0)
    theory_obtained_marks = models.PositiveIntegerField(default=0)

    # Practical marks
    practical_full_marks = models.PositiveIntegerField(default=0)
    practical_pass_marks = models.PositiveIntegerField(default=0)
    practical_obtained_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.profile.user.username} - Sem {self.semester} - {self.subject}"

SEMESTER_SUBJECT_MAP = {
    1: [
        "Mathematics I", "Physics", "English for Technical Communication",
        "Computer Programming", "Fundamental of Computing Technology", "Engineering Drawing I"
    ],
    2: [
        "Mathematics II", "Chemistry", "Engineering Mechanics",
        "Engineering Drawing II", "Environmental Science", "Workshop Practice"
    ],
    3: [
        "Data Structures", "Database Management System", "Operating System",
        "Computer Networks", "Artificial Intelligence", "Machine Learning"
    ],
    # add other semesters if needed
}

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_internal_marks(sender, instance, created, **kwargs):
    if created:
        # For example, create all subjects for semester 1 on profile creation
        semester = 1  # or set dynamically
        subjects = SEMESTER_SUBJECT_MAP.get(semester, [])
        for subject in subjects:
            # Check if it already exists
            if not InternalMark.objects.filter(profile=instance, semester=semester, subject=subject).exists():
                InternalMark.objects.create(
                    profile=instance,
                    semester=semester,
                    subject=subject,
                    theory_full_marks=100,
                    theory_pass_marks=30,
                    practical_full_marks=50,
                    practical_pass_marks=15,
                )

