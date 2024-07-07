from django.contrib import admin

# Register your models here.
from .models import User , Pdf, Remark, PdfAnalysisSummary

admin.site.register(User)
admin.site.register(Pdf)
admin.site.register(Remark)
admin.site.register(PdfAnalysisSummary)