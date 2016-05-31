from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Blogpost

# Create your views here.
def index(request):
    return render_to_response('blogpost/index.html', {'posts':Blogpost.objects.all()[:5]})


def view_post(request, slug):
    return render_to_response('blogpost/blogpost_detail.html', {
        'post': get_object_or_404(Blogpost, slug=slug)
    })
