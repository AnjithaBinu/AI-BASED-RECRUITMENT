from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Work
from .models import Company
from .models import User
from .models import Vacancy
from .models import Appln
from .models import Experience
from .models import Qualification
from .models import Questions
from datetime import date
from django import db
import csv
import time
from django.shortcuts import render
from django.conf import settings
import random
from django.core.files.storage import FileSystemStorage
def csv_simple_write(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_applicants.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'phone_number', 'country'])
    data2 = User.objects.all()
    n2 = len(data2)
    for x in data2:  
        writer.writerow([x.firstname,x.qualification,x.qualification, x.lastname])
       

    return response
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        Id = request.POST.get('id')
        filename = fs.save(Id+".csv", myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, r'pronotes\companyUpload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    else:
        return render(request, r'pronotes\companyUpload.html')
def uploadvVal(request):
    if request.method == 'POST' and request.FILES['applicantcsv']:
        myfile = request.FILES['applicantcsv']
        return redirect('/shortlists')
def uploadvtest(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        Id = request.POST.get('id')
        filename = fs.save("vaccancy/"+Id+".csv", myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, r'pronotes\vUpload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    else:
        return render(request, r'pronotes\vUpload.html')
def index(request):
    newwork = request.POST.get('work')
    if request.method == 'POST':
        work = Work(work=newwork)
        work.save()
        data = Work.objects.all()
        n = len(data)
        parmas = {'range': n, 'data': data}
        return render(request, r'pronotes\index.html', parmas)
    else:
        data = Work.objects.all()
        n = len(data)
        parmas = {'range': n, 'data': data}
        return render(request, r'pronotes\index.html', parmas)
def Vdelete(request,id):
    if request.method == 'GET':
        db.connections.close_all()
        instance = Vacancy.objects.get(Id=id)
        instance.delete()
        return redirect('/vacancy')
def cvdelete(request,id):
    if request.method == 'GET':
        db.connections.close_all()
        instance = Vacancy.objects.get(Id=id)
        instance.delete()
        return redirect('/cvacancies')
def cdelete(request,id):
    if request.method == 'GET':
        db.connections.close_all()
        instance = Company.objects.get(Id=id)
        instance.delete()
        return redirect('/companies')
def cactivate(request,id):
    if request.method == 'GET':
        db.connections.close_all()
        instance = Company.objects.get(Id=id)
        instance.isActive=1;
        instance.save();
        return redirect('/complist')
def udelete(request,id):
    if request.method == 'GET':
        db.connections.close_all()
        instance = User.objects.get(id=id)
        instance.delete()
        return redirect('/candlist')
def delete(request):
    if request.method == 'GET':
        work = request.GET.get('work')
        print(work)
        parmas = {'work' : work}
        instance = Work.objects.get(work=work)
        instance.delete()
        return render(request, r'pronotes\delete.html', parmas)
def home(request):
        return render(request, r'pronotes\home.html')
def login(request):
        return render(request, r'pronotes\login.html')
def dashboard(request):
        data = Experience.objects.all().filter()
        parmas = {'vacancies': data,'name': request.session['name']}
         
                         
        return render(request, r'pronotes\dashboard.html',parmas)
def company(request):
        return render(request, r'pronotes\company.html')
def comp_register(request):
        CompanyName = request.POST.get('company')
        Location = request.POST.get('location')
        ContactPerson = request.POST.get('contact')
        ContactNumber = request.POST.get('phone')
        Email = request.POST.get('email')
        Website  = request.POST.get('website')
        LoginName = request.POST.get('login')
        Password  = request.POST.get('password')
        if request.method == 'POST':
            comp = Company(CompanyName=CompanyName,Location=Location,ContactPerson=ContactPerson,ContactNumber=ContactNumber,Email=Email,Website=Website,LoginName=LoginName,Password=Password)
            comp.save()
            data = Company.objects.all()
            n = len(data)
            parmas = {'range': n, 'data': data}  
        return render(request, r'pronotes\company_save.html', parmas)
def check_login(request):
      return render(request, r'pronotes\company.html')
def saveExperience(request):
    CompanyName = request.POST.get('company')
    Designation = request.POST.get('designation')
    StartDate = request.POST.get('startdate')
    EndDate = request.POST.get('enddate')
    UserId = request.session['userId']
    exp = Experience(CompanyName=CompanyName, Designation=Designation, StartDate=StartDate,EndDate=EndDate,UserId=UserId)
    exp.save()
    return render(request, r'pronotes\experience.html')
def addExperience(request):

    return render(request, r'pronotes\experience.html')
def cvsave(request):

    if request.method == 'POST':
        comp = Company(CompanyName=CompanyName, Location=Location, ContactPerson=ContactPerson,
                       ContactNumber=ContactNumber, Email=Email, Website=Website)
        comp.save()
    return redirect('/dashboard')
def cvapply(request,id):
    instance = User.objects.all().filter(Id=id).first()
    appln = Appln(vid=id, uid=request.session['userId'],name=instance.firstname,qualification=instance.qualification,email=instance.emalid)
    appln.save()
    return render(request, r'pronotes\cvapply.html')
def dashboard(request):
        data = Vacancy.objects.all()
        data2 = Experience.objects.all().filter(UserId=request.session['userId'])
        data3 = Qualification.objects.all().filter(UserId=request.session['userId'])
        parmas = {'vacancies': data,'Experience':data2,'Qualification':data3}
        return render(request, r'pronotes\dashboard.html',parmas)

def admin_login(request):
    
        
        
      return render(request, r'pronotes\admin-login.html')
def comp_login(request):

	
	return render(request, r'pronotes\comp-login.html')

def comp_check_login(request):
        if request.method == 'POST':
            login = request.POST.get('login')
            password = request.POST.get('password')
            try:
                instance = Company.objects.filter(LoginName=login).first()
                if not instance:
                    return redirect('/comp_login')
                
                else:
                    if instance.Password == password:
                        request.session['company'] = instance.CompanyName
                        request.session['companyId'] = instance.Id
                        return redirect('/cdashboard')
                            

                    
                    else:
                        return redirect('/comp_login')
            except:
                return redirect('/comp_login')
        else:
                return redirect('/comp_login')
                    
def admin_check_login(request):
        if request.method == 'POST':
            login = request.POST.get('login')
            password = request.POST.get('password')
            if login == 'admin':
                if password == 'admin':
                    return redirect('/admin_dash')
                else:
                    return redirect('/admin')
            else:
                return redirect('/admin')
def cvapplicants(request):
        data = Vacancy.objects.all()
        n = len(data)
       
        data2 = User.objects.all()
        n2 = len(data2)
        name = request.session['company']
        companyId = request.session['companyId']
        parmas = {'range': n, 'data': data,'range2': n2, 'data2': data2,'name':name }
        return render(request, r'pronotes\cvapplicants.html',parmas)               
def cdashboard(request):
        data = Vacancy.objects.all()
        n = len(data)
       
        data2 = User.objects.all()
        n2 = len(data2)
        name = request.session['company']
        companyId = request.session['companyId']
        parmas = {'range': n, 'data': data,'range2': n2, 'data2': data2,'name':name }
        return render(request, r'pronotes\companyDashboard.html',parmas)
def admin_dash(request):
        
    return render(request, r'pronotes\adminDashboard.html')
def vacancies(request):
        data = Vacancy.objects.all()
        n = len(data)       
        parmas = {'range': n, 'data': data }  
        return render(request, r'pronotes\vacancyList.html',parmas)
def cvacancyTestData(request):
    id=request.session['companyId']
    data = Vacancy.objects.all().filter(compid=id)
    n = len(data)
    parmas = {'range': n, 'data': data}
    return render(request, r'pronotes\cvacancyTestData.html', parmas)
def shortlist(request):
    id=request.session['companyId']
    data = Vacancy.objects.all().filter(compid=id)
    n = len(data)
    parmas = {'range': n, 'data': data}
    return render(request, r'pronotes\shortlist.html', parmas)
def compvacancies(request):
    id=request.session['companyId']
    data = Vacancy.objects.all().filter(compid=id)
    n = len(data)
    parmas = {'range': n, 'data': data}
    return render(request, r'pronotes\cvacancyList.html', parmas)
def questions(request):
        data = Questions.objects.all()
        n = len(data)       
        parmas = {'range': n, 'data': data }  
        return render(request, r'pronotes\questions.html',parmas)
def capplicants(request,id):
        data = Company.objects.all()
        n = len(data)       
        parmas = {'range': n, 'data': data }  
        return render(request, r'pronotes\companyList.html',parmas)
def companies(request):
        data = Company.objects.all()
        n = len(data)       
        parmas = {'range': n, 'data': data }  
        return render(request, r'pronotes\companyList.html',parmas)
def candidates(request):
        data = User.objects.all()
        n = len(data)
        parmas = {'range': n, 'data': data}  
        return render(request, r'pronotes\candidates.html',parmas)

def results(request):
      return render(request, r'pronotes\results.html')
def testdata(request,id):
      if request.method == 'GET':
        parmas = {'comp': id }
        return render(request, r'pronotes\companyUpload.html',parmas)
def vtestdata(request,id):
      if request.method == 'GET':
        params = {'vac': id }
        return render(request, r'pronotes\vUpload.html',params)
def register(request):
      if request.method == 'GET':
        
        return render(request, r'pronotes\register.html')
def check(request):
            
          if request.method == 'POST':
                login = request.POST.get('login')
                password = request.POST.get('password')
                try:
                    instance = User.objects.filter(LoginName=login).first()
                    if not instance:
                        return redirect('/login')
                    
                    else:
                        if instance.Password == password:
                            request.session['name'] = instance.firstname
                            parmas = {'name': instance.firstname }
                            request.session['userId'] = instance.Id
                            return redirect('/dashboard')
                                

                        
                        else:
                            return redirect('/login')
                except:
                    return redirect('/login')
           
def save(request):
      firstname = request.POST.get('firstname')
      lastname = request.POST.get('lastname')
      qualification = request.POST.get('qualification')
      mobile = request.POST.get('mobile')
      gender = request.POST.get('gender')
      email  = request.POST.get('email')
	  
      LoginName  = request.POST.get('login')
      Password  = request.POST.get('password')
      if request.method == 'POST':
          user = User(firstname=firstname,lastname=lastname,qualification=qualification,emalid=email,LoginName=LoginName,Password=Password)
          user.save()
         
      return render(request, r'pronotes\user_save.html')
def vacancy(request):
      
      return render(request, r'pronotes\vacancy.html')
def addVacancy(request):
      Designation = request.POST.get('designation')
      BasicQualifications = request.POST.get('qualification')
      EndDate = request.POST.get('enddate')
      compid = request.session['companyId']
     
      if request.method == 'POST':
          vacancy = Vacancy(Designation=Designation,BasicQualifications=BasicQualifications,EndDate=EndDate,compid=compid)
          vacancy.save()
          return redirect('/cvacancies')
         
      return redirect('/vacancy')
def saveQualification(request):
    Qual = request.POST.get('Qualification')
    Institution = request.POST.get('Institution')
    University = request.POST.get('University')
    JoiningYear = request.POST.get('joiningdate')

    UserId = request.session['userId']

    if request.method == 'POST':
        qualification = Qualification(Qualification=Qual, Institution=Institution, University=University,
                                JoiningYear=JoiningYear,UserId=UserId)
        qualification.save()

    return redirect('/addQualification')
def exp(request,id):
    data = Experience.objects.all().filter(UserId=id)
    parmas = {'data': data,'uid':id } 
    return render(request,r'pronotes\exp.html',parmas)
def addQualification(request):
    return render(request, r'pronotes\addQualification.html')

def qualifications(request):
    return redirect('/addQualification.html')
def details(request,id):
    data = Qualification.objects.all().filter(UserId=id)
    parmas = {'data': data,'uid':id } 
    return render(request,r'pronotes\details.html',parmas)
def capplicants(request,id):
    data = Appln.objects.all().filter(vid=id)
    parmas = {'data': data } 
    return render(request,r'pronotes\cvapplicants.html',parmas)
def logout(request):
    request.session.flush()
    return redirect('/login')
def shortlists(request):
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.naive_bayes import GaussianNB
    X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
    # define the model
    model = GaussianNB()
    # fit the model
    model.fit(X, y)
    # select a single sample
    Xsample, ysample = [X[0]], y[0]
    items = Appln.objects.order_by('?')[2]
        
    parmas = {'data': items } 
    return render(request,r'pronotes\cvapplicant.html',parmas)
def complogout(request):
    request.session.flush()
    return redirect('/comp_login')
def admlogout(request):
    request.session.flush()
    return redirect('/')
    
