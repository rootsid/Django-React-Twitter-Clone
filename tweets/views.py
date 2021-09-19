from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse, JsonResponse
import random
from tweetme2.rest_api.dev import DevAuthentication
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import is_safe_url
from django.conf import settings
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'tweets/home.html', context={}, status=200)


def tweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweetId": tweet_id})


def tweets_profile_view(request, username, *args, **kwargs):
    return render(request, "tweets/profile.html", context={"profile_username": username})
