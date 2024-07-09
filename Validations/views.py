from django.shortcuts import render
from pandas import read_json
from import_data1.models import import_data1
from import_data1.views import data_creation
from upload.views import save_file_name
from re import search
# Create your views here.
def validation_on_datasets(request,*args,**kwargs):
    df=data_creation.data
    #print(df)
    if len(df)==0:
        return render(request,"Error_google.html",{"Error":"There is no any dataset downloaded upto now"})
    else:
        df2=read_json("/Users/manojkumarsharma/Desktop/Pro_Project/infosys/infosys_project copy 4/media/"+save_file_name.file_name)
       
        #checking weather user is giving more number of columns in a single json
        if len(list(df2))>1:
            n=len(list(df2))
            print("please send {0} json files".format(n))
            #please write exit code here

        #checking weather the user given range or not
        try:
            a,b=[int(x) for x in df2.loc["range",list(df2)[0]].split("-")]
        except KeyError:
            #print("you did not specifed the range there fore we will consider deafult range")
            
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
        a=0

        #using search method here
        for i in li:
            try:
                if search(re,str(i)):

                    #print(search(re,str(i)))
                    
                    ans.append([1,i])
                else:
                    ans.append([0,i])
            except TypeError:
                #print(i)
                #print("The type of the object is not string")
                break
        if not ans:
            return render(request,"Error_google.html",{"Error":"seems you did not found your searching item. Please a valid regex"})
        else:
            #print(ans)
            #print(not_ans)
            a=0
            my_data={"data_wanted":ans,"cols":list(df2)}
            return render(request,"validation_table.html",my_data)
    #this is excuted here i have to add anao
    return render(request,"Error_google.html",{"Error":"There is no any dataset downloaded upto now"})
