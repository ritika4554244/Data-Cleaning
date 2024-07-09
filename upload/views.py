from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .models import upload_files

save_file_name=upload_files
class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            if "sample" in name:
                context["file"]=1
            elif "cleaning" in name:
                context["file"]=0
            else:
                return render(request,"Error_google.html",{"Error":"Sorry enter the file names as per instructions"})
            context['url'] = fs.url(name)
            print(context["url"])
            save_file_name.file_name=name
            print(save_file_name)
            
    except:
        return render(request,"Error_google.html",{"Error":"Seems you did not uploaded the file please upload the file"})
    return render(request, 'upload.html', context)

# Create your views here.
