from django.shortcuts import render
from pandas import read_json
from import_data1.models import import_data1
from import_data1.views import data_creation
from upload.views import save_file_name
from .models import download_dataset
from re import search
# Create your views here.

dowonload_file=download_dataset()

def cleaning_mode(df2,df,column_cleaning):
    mode_value=df[column_cleaning].mode()[0]
    df[column_cleaning].fillna(mode_value,inplace=True)

def cleaning_mean(df2,df,column_cleaning):
    try:
        if df2.loc["data_type",list(df2)[0]]=="int":
            mean_value=int(df[column_cleaning].mean())
            print(mean_value)
            df[column_cleaning].fillna(mean_value,inplace=True)
        else:
            mean_value=(df[column_cleaning].mean())
            df[column_cleaning].fillna(mean_value,inplace=True)
    except:
        mean_value=(df[column_cleaning].mean())
        df[column_cleaning].fillna(mean_value,inplace=True)
def cleaning_dataset(request,*args,**kwargs):
    df=data_creation.data.copy()
    #print(df)
    if len(df)==0:
        return render(request,"Error_google.html",{"Error":"There is no any dataset downloaded upto now"})
    try:
        df2=read_json("/Users/manojkumarsharma/Desktop/infosys_project/media/"+save_file_name.file_name)
        column_cleaning=list(df2)[0]
        li=[]

        #the content is pasted in scrap of infosys_project..

        try:
            if df2.loc["columns",list(df2)[0]]=="all":
                n=0
                for i in list(df):
                    if df[i].isnull().sum()>0:
                        li.append(i)
                        n+=1
                    else:
                        continue
        except:
            n=1
            li.append(column_cleaning)
        for i in range(n):
                if df[li[i]].dtype==str or df[li[i]].dtype=="object":
                    cleaning_mode(df2,df,li[i])
                elif df2.loc["method",list(df2)[0]]=="mean":
                    cleaning_mean(df2,df,li[i])
                elif df2.loc["method",list(df2)[0]]=="mode":
                    cleaning_mode(df2,df,li[i])
                else:
                    return render(request,"Error_google.html",{"Error":"please enter valid method to fill the null values"})
         
        cols_data=data_creation.columns
        dowonload_file.data_final=df
        #print(cols_data)

        li=[]
        min_rows=int(df.shape[0]*0.2)
        for i in range(min_rows):
            li.append(list(df.loc[i][cols_data]))
        my_data={"data":li,"cols":cols_data}
        return render(request,"show_cleaning_dataset.html",my_data)
        
    except:
        return render(request,"Error_google.html",{"Error":"Seems your json file did not uploaded"})