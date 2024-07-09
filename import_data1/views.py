from django.http import HttpResponse
from django.shortcuts import render
from pandas import read_csv,read_excel,read_sql,read_json,DataFrame
from re import search
from pymysql import connect
from .models import import_data1
from .models import import_data1, download_dataset

#from __future__ import print_function

import os.path


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account
dowonload_file=download_dataset()

data_creation=import_data1()
# Create your views here.
#Here we are going to render home page of our project
def home_view(request,*args,**kwargs):
    return render(request,"about.html",{})



#this is the functions will redirect to the appropriate page for requesting of datasets
def site(request):
    return render(request,"about.html",{})
def csv_dataset(request):
    return render(request,"csvimport.html",{})
def excel_dataset(request):
    return render(request,"excelimport.html",{})
def database_dataset(request):
    return render(request,"mysqlimport.html",{})
def googlesheets_dataset(request):
    return render(request,"googlesheetsimport.html",{})

#the following method will trime the dataset string colums
def trim(dataset):
  trim=lambda x: x.strip().title() if type(x) is str else x
  return dataset.applymap(trim)

#this methods are used to import the data
def csv_importing_data(request,*args,**kwargs):
    file_name="/Users/manojkumarsharma/Desktop/Pro_Project/infosys/csv_d/"+request.POST.get('fname')
    data_creation.file_name=request.POST.get('fname')
    #print(file_name)
    try:
        df=trim(read_csv(file_name))
        data_creation.data=df
        cols_data=list(data_creation.data.columns)
        my_data={"cols":cols_data}
        return render(request,"show_cols.html",my_data)
    except:
        err="Seems the dataset you searced here is not found sorry"
        return render(request,"Error_google.html",{"Error":err})

def excel_importing_data(request,*args,**kwargs):
    file_name="F:/DATASETS/EXCEL/"+request.POST.get('fname')
    data_creation.file_name=request.POST.get('fname')
    #print(file_name)
    try:
        df=trim(read_excel(file_name))
        print(df.columns)
        data_creation.data=df
        cols_data=list(data_creation.data.columns)
        my_data={"cols":cols_data}
        return render(request,"show_cols.html",my_data)
    except:
        err="Seems the dataset you searced here is not found sorry"
        return render(request,"Error_google.html",{"Error":err})
def data_base_importing_data(request,*args,**kwargs):
    #selecting database
    data_base=connect(host="localhost",user="root",passwd="Harikrishna1.",database="infosy_project")
    

    #this below code snipt will check whether the searching table is in database or not
    #if it is in database then go on ti next step    
    # django_migrations    
    table_name=request.POST.get('fname')
    data_creation.file_name=table_name
    print(request)
    #table_name=(table_name,)

    #this code snipt comes under the if: condition
    #table_name.strip()
    #query="select * from "+table_name
    query="select * from "+table_name
    cur=data_base.cursor()
    cur.execute(query)


    tables=cur.fetchall()
    df=trim(read_sql(query,data_base))
    data_creation.data=df
    cols_data=list(df.columns)
    my_data={"cols":cols_data}
    return render(request,"show_cols.html",my_data)
def googlesheets_importing_data(request,*args,**kwargs):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'C:/infosys_project/import_data1/keys.json'
    creds=None
    creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #SAMPLE_SPREADSHEET_ID = '1542UZfstkZEevRejf3YbA_Upk5s05WK-YIPjBAl3SYY'
    SAMPLE_SPREADSHEET_ID = request.POST.get("fname")
    data_creation.file_name=SAMPLE_SPREADSHEET_ID
    Sheet_range=request.POST.get('range')
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        
        #this is for reading 
        #"Sheet1!A1:I95"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=Sheet_range).execute()
        #list=[["haell",400],["erwe",4563]]
        #this is for writing
        #request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet2!B1", valueInputOption="USER_ENTERED", body={"values":list}).execute()
        #print(result)

        #this is for conversion of sheet to dataframe
        df=trim(DataFrame(result["values"]))
        df.columns=result["values"][0]
        df=df.drop(0)
        df.reset_index(drop=True,inplace=True)
        cols_data=list(df.columns)
        data_creation.data=df
        my_data={"cols":cols_data}
        return render(request,"show_cols.html",my_data)
    except HttpError as err:
        return render(request,"Error_google.html",{"Error":err})
    
#the following method is used to show the dataset in the table form by masking the columns that are given by
#the user
def validation_datasets(request,*args,**kwargs):
    df=data_creation.data
    if len(df)==0:
        return render(request,{"Error":"There is no any dataset downloaded upto now"})
    else:
        df2=read_json("/Users/manojkumarsharma/Desktop/sample12.json")
        #checking weather user is giving more number of columns in a single json
        if len(list(df2))>1:
            n=len(list(df2))
            print("please send {0} json files".format(n))
        #checking weather the user given range or not
        try:
            a,b=[int(x) for x in df2.loc["range",list(df2)[0]].split("-")]
        except KeyError:
            print("you did not specifed the range there fore we will consider deafult range")
            a=0
            if df.shape[0]>200:
                b=int(0.2*df.shape[0])
            else:
                b=df.shape[0]

        #getting wanted number of rows for the user
        wanted=df.iloc[a:b]
        re=df2.loc["expression"][list(df2)[0]]


        #getting the values of that column into a form of list
        li=list(wanted[list(df2)[0]])
        ans=[]
        not_ans=[]
        bin=[]
        access=[]
        a=0
        j=0

        #using search method here
        for i in li:
            try:
                if search(re,str(i)):
                    print(search(re,str(i)))
                    ans.append([1,i])
                else:
                    ans.append([0,i])
            except TypeError:
                print(i)
                print("The type of the object is not string")
                break
        if not ans:
            return render(request,"Error_google.html",{"Error":"seems you did not found your searching item. Please a valid regex"})
        else:
            print(ans)
            print(not_ans)
            a=0
            my_data={"data_wanted":ans,"cols":list(df2)}
            return render(request,"validation_table.html",my_data)
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


def cleaning_data(request,*args,**kwargs):
    df=data_creation.data.copy()
    #print(df)
    if len(df)==0:
        return render(request,"Error_google.html",{"Error":"There is no any dataset downloaded upto now"})
    # try:
    df2=read_json("/Users/manojkumarsharma/Desktop/cleaning12.json")
    column_cleaning=list(df2)[0]
    li=[]
    if df2.loc["columns",list(df2)[0]]=="all":
        n=0
        for i in list(df):
            if df[i].isnull().sum()>0:
                li.append(i)
                n+=1
            else:
                continue
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
         
    cols_data=df.columns
        
    dowonload_file.data_final=df
    li=[]
    min_rows=int(df.shape[0]*0.2)
    for i in range(min_rows):
        li.append(list(df.loc[i][cols_data]))
    my_data={"data":li,"cols":cols_data}
    return render(request,"Clean.html",my_data)


def view_data(request,*args,**kwargs):
    #return HttpResponse("<h1>Hello World</h1>")

    #if the columns for masking is not given then the length of the column name will be 0
    column=request.POST.get('fname')
    if "," in column:
        cols=column.split(",")
        n=len(cols)
    else:
        cols=[column]
        n=1
    try:
        """df=read_csv(file_name)
        data_creation.data=df"""
        cols_data=list(data_creation.data.columns)
        if len(column)>0:
            #cols_data.remove(column)
            for i in range(n):
                cols_data.remove(cols[i])
        #print(cols_data)
        df=data_creation.data.copy()
        data_creation.columns=cols_data
        li=[]
        min_rows=int(df.shape[0]*0.2)
        for i in range(min_rows):
            li.append(list(df.loc[i][cols_data]))
        my_data={"data":li,"cols":cols_data}
        return render(request,"show.html",my_data)
    except:
        err="Seems there is an error found sorry"
        return render(request,"Error_google.html",{"Error":err})
    
def view(request,*args,**kwargs):
    #return HttpResponse("<h1>Hello World</h1>")
     return render(request,"mask.html",{})
  
def csv_dataset(request):
    return render(request,"csvimport.html",{})
def excel_dataset(request):
    return render(request,"excelimport.html",{})
def database_dataset(request):
    return render(request,"mysqlimport",{})
def googlesheets_dataset(request):
    return render(request,"GoogleSheet.html",{})
def validate_dataset(request):
    return render(request,"ValidationTable.html",{})

    