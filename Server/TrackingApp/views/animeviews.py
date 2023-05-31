from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import serializers

from TrackingApp.models import Anime,User,Episode
from TrackingApp.serializer import AnimeSerializer,UserSerializer,EpisodeSerializer
from TrackingApp.services import animeservices

# Create your views here.

# Anime Model and APIs 
# Get Anime List with filter    
@csrf_exempt
def animeAPI(request):
    if request.method == 'GET':
        data = getAnimesByName(request)
    if request.method == 'POST':
        data = postAnime(request)
    if request.method == 'DELETE':
        data = deleteAnime(request)
    return data

def getAnimesByName(request):
    name = request.GET.get('name')
    data = animeservices.getAnimesByName(name)
    print(data)
    return JsonResponse(data,safe=False)

def getAnimeByID(request,animeID):
    if request.method == 'GET':
        data = animeservices.getAnimeByID(animeID)
        print(data)
        return JsonResponse(data,safe=False)
    pass

def getAnimeListByUserID(request, userID):
    if request.method == 'GET':
        data = animeservices.getAnimeListByUserID(userID)
        return JsonResponse(data,safe=False)
    pass

def displayAnimeList(request):
    # Needs User ID
    if request.method == 'GET':
        animes = Anime.objects.all()
        anime_serializer = AnimeSerializer(animes, many=True)
        return JsonResponse(anime_serializer.data,safe=False)
    pass

def postAnime(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        status = animeservices.addAnime(data)
    return status

def deleteAnime(request):
    # Delete Anime from personal list
    # Needs User ID
    if request.method == "DELETE":
        data = JSONParser().parse(request)
        status = animeservices.deleteAnime(data)
    return status


@csrf_exempt
def episodeAPI(request,id):
    if request.method == 'GET':
        data = getEpisodeList(request,id)
    elif request.method == 'POST':
        data = postEpisode(request)
    elif request.method == 'DELETE':
        data = deleteEpisode(request)
    return data

def getEpisodeList(request,id):
    if request.method == 'GET':
        episodes = Episode.objects.filter(anime_id = id)
        episode_serializer = EpisodeSerializer(episodes, many= True)
        return JsonResponse(episode_serializer.data,safe=False)

def postEpisode(request):
    data = JSONParser().parse(request)
    status = animeservices.addEpisode(data)
    return status
    
def deleteEpisode(request):
    data = JSONParser().parse(request)
    status = animeservices.deleteEpisode(data)
    return status
