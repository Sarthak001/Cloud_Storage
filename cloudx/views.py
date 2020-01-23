from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserDetails, FileDetails
from django.core.files.storage import FileSystemStorage
import os, time
import hashlib
import mimetypes
# Create your views here.

def index(request):
    if('email' in request.session):
        user1 = UserDetails.objects.get(email=request.session['email'])
        location = 'D:/web/UserUploads/' + user1.email + '/'
        l = []
        for f in FileDetails.objects.filter(user=user1.email).all():
            l.append(f)
        u = {'UserFiles':l, 'UserDetails':user1}
        return render(request,'index.html', u)
    else:
        messages.info(request, 'Please login')
        return redirect('/login/')

def logout(request):
    del request.session['email']
    return render(request,'login.html')

def register(request):
    if(request.method == 'POST'):
        firstName = request.POST['fname']
        lastName = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["pass"]
        address = request.POST['address']
        city = request.POST['city']
        country = request.POST['country']
        md5_password = hashlib.md5(password.encode())
        encrypt_password = md5_password.hexdigest()

        if(UserDetails.objects.filter(email=email).exists()):
            return HttpResponse('email')
        else:
            detail = UserDetails(password=encrypt_password, email=email, firstName=firstName, lastName=lastName, address=address, city=city, country=country)
            detail.save()
            return HttpResponse("successful")
    else:
        return render(request,"register.html")

def forgot_password(request):
    return render(request,'forgot-password.html')

def profile(request):
    if('email' in request.session):
        user = UserDetails.objects.get(email=request.session['email'])
        return render(request,'profile.html', {'UserDetails': user})
    else:
        messages.info(request, 'Please login')
        return redirect('/login/')

def cloud(request):
    return render(request,'cloud.html')

def home(request):
    return render(request,'home.html')

def login(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        md5_password = hashlib.md5(password.encode())
        encrypt_password = md5_password.hexdigest()
        
        user = UserDetails.objects.get(email=email)
        if(user.password == encrypt_password):
            request.session['email'] = email
            u1 = {'UserDetails': user}
            return render(request, 'index.html', u1)
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def upload(request):
    if('email' in request.session):
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            if(FileDetails.objects.filter(fileName=uploaded_file.name).exists()):
                messages.info(request, 'file with same name exists')
                return redirect('index')
            user = UserDetails.objects.get(email=request.session['email'])
            fs = FileSystemStorage(location='D:/web/UserUploads/' + str(user.email) + '/')
            fs.save(uploaded_file.name,uploaded_file)
            details = os.stat('D:/web/UserUploads/' + str(user.email) + '/' + uploaded_file.name)
            size = details.st_size
            if((int(size)//1024) < 1):
                size = str(size) + ' bytes'
            elif((int(size)//(1024*1024)) < 1):
                size = str((int(size)//1204)) + ' KB'
            else:
                size = str((int(size)//(1204*1024))) + ' MB'
            f = FileDetails(fileName=uploaded_file.name, user=user.email, lastModified=time.ctime(details.st_mtime), size=size)
            f.save()
            return redirect('index')
        else:
            return render(request,'upload.html')
    else:
        messages.info(request, 'Please login')
        return render(request,'login.html')

def uploadProfile(request):
    if('email' in request.session):
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            user = UserDetails.objects.get(email=request.session['email'])
            if(user.email +'.jpeg' in os.listdir('D:/web/cloud/cloudx/static/assets/img/profile/')):
                os.remove('D:/web/cloud/cloudx/static/assets/img/profile/' + str(user.email) + '.jpeg')
            fs = FileSystemStorage(location='D:/web/cloud/cloudx/static/assets/img/profile/')
            fs.save(uploaded_file.name,uploaded_file)
            os.rename('D:/web/cloud/cloudx/static/assets/img/profile/' + str(uploaded_file.name), 'D:/web/cloud/cloudx/static/assets/img/profile/' + user.email + '.jpeg')
            return redirect('profile')
        else:
            return render(request,'profile.html')
    else:
        messages.info(request, 'Please login')
        return render(request,'login.html')

def updatedetails(request):
     if(request.method == 'POST'):
        f_name = request.POST['first_name']
        l_name = request.POST["last_name"]
        detail = UserDetails.objects.filter(email=request.session['email'])
        detail.firstName = f_name
        detail.lastName = l_name
        detail.update(firstName=f_name,lastName=l_name)
        return redirect('profile')
     else:
        return render(request,'profile.html')

def newfile(request):
    if(request.method == 'POST'):
        filename = request.POST['file_name']
        data = request.POST['data']
        user = UserDetails.objects.get(email=request.session['email'])
        f = open('D:/web/UserUploads/' + str(user.email) + '/' + filename + '.txt', 'w' )
        f.write(data)
        f.close()

        return redirect('index')
    else:
        return redirect('index')
    

def updatedetails2(request):
    if(request.method == 'POST'):
        address = request.POST['address']
        city = request.POST["city"]
        country = request.POST["country"]
        detail = UserDetails.objects.filter(email=request.session['email'])
        detail.address = address
        detail.city = city
        detail.country = country
        detail.update(address=address,city=city,country=country)
        return redirect('profile')
    else:
        return render(request,'profile.html')

        
def download(request):
    if (request.method =='POST'):    
        File = request.POST.get('select',False)
        user = UserDetails.objects.get(email=request.session['email'])
        location = 'D:/web/UserUploads/' + str(user.email) + '/' + File
        file_type , b =  mimetypes.guess_type(location)
        final = f'attachment;filename = {File}'
    response = HttpResponse(open(location, 'rb').read())
    response['Content-Type'] = file_type
    response['Content-Disposition'] = final
    return response

def delete(request):
    if (request.method =='POST'):    
        File = request.POST.get('select',False)
        user = UserDetails.objects.get(email=request.session['email'])
        if(File in os.listdir('D:/web/UserUploads/' + user.email + '/')):
            location = 'D:/web/UserUploads/' + str(user.email) + '/'
            path = os.path.join(location,File)
            os.remove(path)
            if FileDetails.objects.filter(user=request.session['email']):
                FileDetails.objects.filter(fileName=File).delete()
            return redirect('index')
        else:
            return redirect('index')

def view_file(request):
    if(request.method == 'POST'):
        File = request.POST.get('select',False)
        user = UserDetails.objects.get(email=request.session['email'])
        location = 'http://127.0.0.1:8000/media/'+ str(user.email)+ '/' + File
        return redirect(location)
