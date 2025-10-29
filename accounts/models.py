from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model with role-based permissions."""
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_STUDENT, 'Student'),
        (ROLE_USER, 'Regular User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def is_teacher(self) -> bool:
        """Check if user has teacher role."""
        return self.role == self.ROLE_TEACHER

    def is_student(self) -> bool:
        """Check if user has student role."""
        return self.role == self.ROLE_STUDENT

    def __str__(self) -> str:
        return self.username
