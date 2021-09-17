from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse, JsonResponse
import random
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from tweetme2.rest_api.dev import DevAuthentication
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import is_safe_url
from django.conf import settings
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'tweets/home.html', context={}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    # qs = Tweet.objects.filter(user__username=user)
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([DevAuthentication, SessionAuthentication])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.filter(id=tweet_id, user__username=user)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([DevAuthentication])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.filter(id=tweet_id, user__username=user)
    if not qs.exists():
        return Response({"message": "You are not aurthorized."}, status=403)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet Removed."}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([DevAuthentication, SessionAuthentication])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required
    Action options are like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")

        user = request.user
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({"message": "You are not aurthorized."}, status=403)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            parent_obj = obj
            new_tweet = Tweet.objects.create(
                user=request.user, parent=parent_obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
        return Response({"message": f"{action}"}, status=200)


def tweet_list_view_pure_django(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.filter(user__username=user)
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data, status=200)


@csrf_exempt
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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


def tweet_create_view_pure_django(request, *args, **kwargs):
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
