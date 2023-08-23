from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from .form import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

# Create your views here.

def userLOgin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd["username"],password=cd["password"])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Login Sucessfull")
                else :
                    return HttpResponse('Account disabled')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form  = LoginForm()
        
    return render(request, "account/login.html",{"form":form})

@login_required()
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id",flat=True)
    
    actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related("user","user__profile").prefetch_related("target")[:10]  #using the select_related and prefetch_related to import the speed by makingnonly a singel querynto the data base and it also join the field in the select_related() to the table so that a new query will not be needed when trying to access the related field
    
    return render(request, "account/dashboard.html",{"section":"dashboard","actions":actions})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user,  'has created an account')
            print(new_user.username)
            
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        form = UserRegistrationForm()
    
    context = {"form": form}
    return render(request, "account/register.html", context)

@login_required()
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files= request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,  'Profile updated successfully')
            return redirect("dashboard")
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {
        "user_form":user_form,
        "profile_form":profile_form,
    }
    return render(request, "account/edit.html",context)
        
    

@login_required()
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',{"section":"people","users":users})

@login_required()
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    print(user.id)
    return render(request, 'account/user/detail.html',{"section":"people","user":user})


@require_POST
@login_required()
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if user != request.user:
                if action == "follow" :
                    Contact.objects.get_or_create(user_from=request.user,user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    Contact.objects.filter(user_from=request.user,user_to=user).delete()
                return JsonResponse({"status":"ok"})
        except User.DoesNotExist:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})
        