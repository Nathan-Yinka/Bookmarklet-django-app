from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from social_core.exceptions import AuthCanceled
from django.shortcuts import redirect
from .models import Profile
from django.db.models import Q

class EmailAuthenticate():
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
    
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def create_profile(backend,user,*args, **kwargs):
    """
    Create user profile for social authentication
    """
    if user:
        Profile.objects.get_or_create(user=user)
 
    
def create_user(backend,details,user,username,*args,**Kwargs):
    if user:
        return {"user":user}
    email = details.get('email')
    if email and User.objects.filter(Q(email=email)|Q(email=username)).exists():
        return None
    user = User.objects.create_user(username=username)
    return {"user":user}