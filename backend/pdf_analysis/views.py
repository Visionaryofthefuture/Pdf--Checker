from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from .forms import PdfUploadForm
from User.models import Pdf
from django.contrib.auth.decorators import login_required

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PdfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit = False)
            pdf.user = request.user
            pdf.save()  
            return redirect('pdf_functions', pdf_id=pdf.pk)
    else:
        form = PdfUploadForm()
    return render(request, 'pdf_analysis/upload_page.html', {'form': form})

def pdf_functions(request, pdf_id):
    pdf = get_object_or_404(Pdf, pk=pdf_id)
    
    return render(request, 'pdf_analysis/pdf_functions.html', {'pdf': pdf})


def check_blank_pages(request, pdf_id):
    pdf = get_object_or_404(Pdf, pk=pdf_id)
    
    return render(request, 'pdf_analysis/pdf_functions.html', {'pdf': pdf})

def detect_page_number_location(request, pdf_id):
    return HttpResponse("Detect Page Number Location functionality")

def find_landscape_pages(request, pdf_id):
    return HttpResponse("Find Landscape Pages functionality")

def check_double_sided(request, pdf_id):
    return HttpResponse("Check if PDF is Double-Sided functionality")

def verify_margin_specification(request, pdf_id):
    return HttpResponse("Check and Verify Margin Specification functionality")

def all_functions(request, pdf_id):
    return HttpResponse("Perform All Functions functionality")
