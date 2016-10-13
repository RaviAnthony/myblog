from urllib import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from .forms import BlogForm

def blog_list(request):
    today = timezone.now().date()
    queryset_list = Blog.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Blog.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).distinct()
    paginator = Paginator(queryset_list,4)
    # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    #import ipdb; ipdb.set_trace()
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset= paginator.page(paginator.num_pages)

    context = {
        "objects_list": queryset,
        "title": "RaviAnthony Blog",
        "page_request_var":page_request_var,
        "today":today,
    }
    return render(request,"post_list.html",context)
    #return HttpResponse("<h1>List</h1>")

def blog_detail(request,slug=None):
    #queryset = Blog.objects.all()
    instance = get_object_or_404(Blog, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {"title": instance.title,
               "instance": instance,
               "share_string":share_string,}
    return render(request, "detail.html", context)

def blog_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = BlogForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request,"successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {"form":form,}
    return render(request, "create.html", context)

def blog_update(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Blog, slug=slug)
    #print instance
    form = BlogForm(request.POST or None, request.FILES or None,instance = instance)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.user=request.user
        instance.save()
        messages.success(request,  "<a href = '#'> Item </a> Saved ",extra_tags='some-tag')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = { "title": instance.title,
                "instance":instance,
                "form":form,
                }
    return render(request, "create.html", context)

def blog_delete(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Blog, slug=slug)
    instance.delete()
    messages.success(request, "Sucessfully deleted")
    return redirect("blog:list")
