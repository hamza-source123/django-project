from django.shortcuts import render
from application1.forms import Userform,Userprofileinfo

## export some packages for login and logout system
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render (request,'application1/index.html')

####################################################

@login_required
def special(request):
# Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("you are logged in!!")

#############################################################

#create logout view
@login_required
def user_logout(request):
    # logout the user
    logout(request)
    #return to home page
    return HttpResponseRedirect(reverse('index'))




#############################################################



###Registration view
def register(request):
    registerd=False
    if request.method=='POST':
        user_form=Userform(data=request.POST)
        user_profile_info=Userprofileinfo(data=request.POST)

        ##Check what data is valid
        if user_form.is_valid() and user_profile_info.is_valid():
            #save data of userform into data base
            user=user_form.save()
            #hash the password
            user.set_password(user.password)
            #update the password
            user.save()

            #now we will deal with exctra information of userprofileinfo class
            profile=user_profile_info.save(commit=False)
            #set one to one relation ship between 
            #User form and User profile form
            profile.user=user

            #working with profile pic
            if 'profile_pic' in request.FILES:
                print("found it")
                # If yes, then grab it from the POST form reply
                profile.profile_pic=request.FILES['profile_pic']
            #now save into model
            profile.save()

            #so registration has been succesfully!!!
            registerd=True

        else:
            print(user_form.errors,user_profile_info.errors)
    else:
        user_form=Userform()
        user_profile_info=Userprofileinfo()

    return render(request,'application1/registration.html',
                            {
                                'user_form':user_form,
                                'profile_form':user_profile_info,
                                'registerd':registerd

                            })



###########################################################



### User login View
def user_login(request):
    if request.method=='POST':
        #first get username and password
        user_name=request.POST.get('username')
        password=request.POST.get('password')


        #now we will use django built in authentication function
        user=authenticate(username=user_name, password=password)

        # if we have user 
        if user:
            #now check account is active
            if user.is_active:
                #login the user
                login(request,user)
                #now we will send user to home page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("your account is not active!!")
        else:
            return HttpResponse("invalid login or password")
    else:
        #nothing has been provided for userame and password
        return render (request,'application1/login.html',{})
