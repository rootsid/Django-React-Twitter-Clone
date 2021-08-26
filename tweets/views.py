from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse, JsonResponse
import random
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import is_safe_url
from django.conf import settings
from .forms import TweetForm
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, 'tweets/home.html', context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.filter(user__username = user)
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data, status=200)


@csrf_exempt
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
        REST API View
        Consume by JS, return JSON Data
    """
    data = {
            "id": tweet_id,
            "content": "",
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
        status = 200
    except:
        data["message"] = "Not found"
        status = 404
    return JsonResponse(data, status=status)


def tweet_create_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user or None
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'tweets/forms.html', context={"form": form})