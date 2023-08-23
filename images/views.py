from django.shortcuts import render,redirect,get_object_or_404
from .form import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Image
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from actions.utils import create_action

# Create your views here.

@login_required()
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.changed_data
            new_image = form.save(commit=False)
            
            #asding the user
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "bookmarked image", new_image)
            
            #asding a message to the user
            messages.success(request, "the image hhas been added")
            
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, "images/image/create.html",{'form':form,"section":"images"})

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    print(image.image.url)
    
    return render(request, 'images/image/detail.html',{'section': 'images','image': image})

@login_required()
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    
    if image_id and action :
        try:
            image  = Image.objects.get(id=int(image_id))
            
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status":"ok"})
        except:
            pass
        return JsonResponse({"status":"error"})
    
@login_required()
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,10)
    page = request.GET.get('page')
    images_only = request.GET.get("images_only")
    
    try:
        images = paginator.page(page)
    
    except PageNotAnInteger:
        images = paginator.page(1)
        
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if images_only: 
        return render(request, "images/image/list_images.html",{"images":images,"section":"images"})
    
    return render(request, "images/image/list.html",{"images":images,"section":"images"})
    