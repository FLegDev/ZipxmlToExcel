from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MultipleZipUploadForm
from .services import import_zip_file
from django.http import HttpResponse
from django.utils.translation import get_language

def upload_multiple_zips(request):
    if request.method == 'POST':
        form = MultipleZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data['files']  # ✅ Plus sûr
            imported_count = 0
            for f in files:
                invoices = import_zip_file(f)
                if invoices:
                    imported_count += len(invoices)
            messages.success(request, f"{imported_count} factures importées avec succès.")
            return redirect('admin:index')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifiez vos fichiers.")
    else:
        form = MultipleZipUploadForm()

    return render(request, 'invoices/upload_multiple_zips.html', {'form': form})

def test_lang_view(request):
    return HttpResponse(f"Langue active : {get_language()}")