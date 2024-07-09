from django.shortcuts import render
from import_data1.views import data_creation
from pandas import DataFrame
from cleaning.views import dowonload_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from .models import file_name
import mimetypes
import os
files=file_name()
def download_csv(request,*args,**kwargs):
    file_name=data_creation.file_name.split(".")[0]
    show_file=file_name+".csv"
    files.filename=show_file
    file_name="/Users/manojkumarsharma/Desktop/download_files/"+file_name+".csv"
    files.thefile=file_name
    df=dowonload_file.data_final
    df.to_csv(file_name,index=True)
    return render(request,"download_dataset.html",{"file_name1":file_name,"show":show_file})
def download_excel(request,*args,**kwargs):
    file_name=data_creation.file_name.split(".")[0]
    show_file=file_name+".xlsx"
    files.filename=show_file
    file_name="F:/Exported_files/EXCEL/"+file_name+".xlsx"
    files.thefile=file_name
    df=dowonload_file.data_final
    df.to_excel(file_name,index=True)
    return render(request,"download_dataset.html",{"file_name1":file_name,"show":show_file})
def download_pdf(request,*args,**kwargs):
    file_name=data_creation.file_name.split(".")[0]
    show_file=file_name+".pdf"
    files.filename=show_file
    file_name="F:/Exported_files/PDF/"+file_name+".pdf"
    files.thefile=file_name
    df=dowonload_file.data_final
    fig, ax =plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    #https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
    pp = PdfPages("foo.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    return render(request,"download_dataset.html",{"file_name1":file_name,"show":show_file})
def downloadfile(request,*args,**kwargs):
    print(files.filename)
    chunk_size=8192
    response=StreamingHttpResponse(FileWrapper(open(files.thefile,"rb"),chunk_size),
                                   content_type=mimetypes.guess_type(files.thefile)[0])
    response["Content-Length"]=os.path.getsize(files.thefile)
    response["Content-Disposition"]="Attachment;filename=%s" % files.filename
    return response
    

# Create your views here.
