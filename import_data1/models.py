from django.db import models
from pandas import DataFrame

# Create your models here.
class import_data1(models.Model):
    data=DataFrame()
    columns=[]
    file_name=""
class download_dataset(models.Model):
    data_final=DataFrame()