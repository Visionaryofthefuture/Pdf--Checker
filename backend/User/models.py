from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from .accounts import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
        error_messages={
    'unique': "A user with that email already exists.",  
        })
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
class Pdf(models.Model):
    pdf = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])], upload_to='media/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.get_full_name()} : {self.pdf.name[6:]}"

class Remark(models.Model):
    pdf = models.ForeignKey(Pdf, on_delete=models.CASCADE, related_name='remarks')
    page_number = models.PositiveIntegerField()
    is_blank = models.BooleanField(default=False)
    page_number_location = models.CharField(max_length=255, blank=True, null=True)
    top_margin = models.FloatField(blank=True, null=True)
    left_margin = models.FloatField(blank=True, null=True)
    bottom_margin = models.FloatField(blank=True, null=True)
    right_margin = models.FloatField(blank=True, null=True)
    orientation = models.CharField(max_length=20, choices=[('Portrait', 'Portrait'), ('Landscape', 'Landscape')], blank=True, null=True)

    def __str__(self):
        return f"Page {self.page_number} Remark for PDF: {self.pdf.pdf.name}"

class PdfAnalysisSummary(models.Model):
    pdf = models.OneToOneField(Pdf, on_delete=models.CASCADE, related_name='analysis_summary')
    blank_pages_count = models.PositiveIntegerField(default=0)
    total_pages = models.PositiveIntegerField(default=0)
    landscape_pages_count = models.PositiveIntegerField(default=0)
    margin_issues_count = models.PositiveIntegerField(default=0)
    double_sided = models.BooleanField(default=False)

    def __str__(self):
        return f"Analysis Summary for PDF: {self.pdf.pdf.name}"