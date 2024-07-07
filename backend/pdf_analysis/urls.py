from django.urls import path
from pdf_analysis import views


urlpatterns = [
    path('pdfupload/', views.upload_pdf, name = "upload_page"),
    path('pdf-functions/<int:pdf_id>/', views.pdf_functions, name='pdf_functions'),
]

urlpatterns += [
    path('check-blank-pages/<int:pdf_id>/', views.check_blank_pages, name='check_blank_pages'),
    path('detect-page-number-location/<int:pdf_id>/', views.detect_page_number_location, name='detect_page_number_location'),
    path('find-landscape-pages/<int:pdf_id>/', views.find_landscape_pages, name='find_landscape_pages'),
    path('check-double-sided/<int:pdf_id>/', views.check_double_sided, name='check_double_sided'),
    path('verify-margin-specification/<int:pdf_id>/', views.verify_margin_specification, name='verify_margin_specification'),
    path('all-functions/<int:pdf_id>/', views.all_functions, name='all_functions'),
]



