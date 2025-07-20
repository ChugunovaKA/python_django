from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 Мб

class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.size > MAX_FILE_SIZE:
                return HttpResponseBadRequest("Ошибка: Файл превышает 1 Мб.")
            with open(f'media/{file.name}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return HttpResponse("Файл успешно загружен!")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})