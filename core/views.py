import logging

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Theatre, Show, Movie, MovieTheatreShow, City
from .serializer import *


@csrf_exempt
@require_http_methods(['POST'])
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return JsonResponse({'status': True, 'message': 'Login Successful'})
        else:
            return JsonResponse({'status': False, 'message': 'Account is disabled'})
    else:
        logging.info("Invalid credentials provided with following username -> %s " % username)
        return JsonResponse({'status': False, 'message': 'Invalid Credentials, You can register from Registration '
                                                         'endpoint'}, status=status.HTTP_401_UNAUTHORIZED)


@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 'disconnected', 'message': 'You have been logged out successfully'})


@csrf_exempt
def customer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        city = request.POST['city']
        print(username, password, city)
        customer = Customer.objects.create_user(username, password, city)
        customer.save()
        logging.info("New customer created : %s" % username)
        return JsonResponse({"status": "Registration Successful"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"status": "Only POST method is allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Get all the movies in your city
@csrf_exempt
def get_all_movies_in_city(request, city_name):
    city_name = city_name.title()
    requested_city = City.objects.filter(city_name=city_name).first()
    if requested_city:
        # Get list of all the theaters in city
        theaters_in_requested_city = Theatre.objects.filter(city=requested_city).values('theater_name').distinct()
        theater_list = []
        if theaters_in_requested_city:
            for theater in theaters_in_requested_city:
                theater_list.append(theater)
            movie_list_json = []

            # Get list of all the movies in a particular theater
            for theater_name in theater_list:
                movies_in_theater = MovieTheatreShow.objects.filter(theatre=theater_name["theater_name"]).values(
                    'movie').distinct()

                for mv in movies_in_theater:
                    movie_n = Movie.objects.filter(movie_name=mv["movie"])
                    for movie in movie_n:
                        movie_serialized = MovieSerializer(movie).data
                        # List only unique movies
                        if movie_serialized not in movie_list_json:
                            movie_list_json.append(movie_serialized)
            return JsonResponse(movie_list_json, safe=False)
        else:
            logging.info("Users requested for movies in city %s" % city_name)
            return JsonResponse({"message": "Currently no theater in the %s city " % city_name})
    else:
        logging.info("Users requested for movies in city %s" % city_name)
        return JsonResponse({"message": "Currently %s is not registered in our cities" % city_name})


def get_theatre_shows_json(list_of_theatre_and_show):
    theatre_shows_map = [
        {'theatre_name': name, 'show_name': [d['show'] for d in list_of_theatre_and_show if d['theatre'] == name]}
        for name in set(map(lambda d: d['theatre'], list_of_theatre_and_show))]
    theatres_list = []
    for theatre_show in theatre_shows_map:
        theatre = Theatre.objects.filter(pk=theatre_show['theatre_name']).first()
        theatre_shows_json = TheatreSerializer(theatre).data
        shows_list_json = []
        for show_name in theatre_show['show_name']:
            show = Show.objects.filter(pk=show_name).first()
            shows_list_json.append(ShowSerializer(show).data)
        theatre_shows_json["shows"] = shows_list_json
        theatres_list.append(theatre_shows_json)
    return theatres_list


# check all cinemas in which a movie is playing along with all the showtimes
@csrf_exempt
def get_cinema_and_show_details_for_movie(request, movie_name):
    movie_name = movie_name.title()
    requested_movie = Movie.objects.filter(movie_name=movie_name).first()

    # get all the theater(cinema) name with show name for the movie
    if requested_movie:
        shows_for_requested_movie = MovieTheatreShow.objects.filter(movie=requested_movie).values('show', 'theatre')

        theater_show_list = []

        print(shows_for_requested_movie)
        for show_in_theater in shows_for_requested_movie:
            theater_show_list.append(show_in_theater)

        theatre_shows_json = get_theatre_shows_json(theater_show_list)
        movie_details_json = MovieSerializer(requested_movie).data
        movie_details_json["theatres"] = theatre_shows_json
        return JsonResponse(movie_details_json, safe=False)
    elif requested_movie is None:
        return JsonResponse({"message": "%s movie is not available" % movie_name})
    logging.error("Available Shows for %s movie cannot be served" % movie_name)
    return JsonResponse({"message": "Sorry we are facing issues from our side"})


# For each show time check the availability of seats
@csrf_exempt
def get_availability_for_all_shows(request):
    show_times = Show.objects.all()

    # get all the theater(cinema) name with show name
    if show_times:

        for show_time in show_times:
            shows_for_requested_movie = MovieTheatreShow.objects.filter(show=show_time).values('show', 'theatre')

            theater_show_list = []

            print(shows_for_requested_movie)
            for show_in_theater in shows_for_requested_movie:
                theater_show_list.append(show_in_theater)

            theatre_shows_json = get_theatre_shows_json(theater_show_list)

            return JsonResponse(theatre_shows_json, safe=False)
    elif show_times is None:
        return JsonResponse({"message": " no show times available"})


# Book a ticket

def book_ticket(request, city_name, movie_name, theatre_name, show_name):
    if request.user.is_authenticated:
        # Normalizing user input data
        city_name, movie_name, theatre_name, show_name = city_name.title(
        ), movie_name.title(), theatre_name.title(), show_name.title()
        city = City.objects.filter(city_name=city_name).first()
        movie = Movie.objects.filter(movie_name=movie_name).first()
        theatre = Theatre.objects.filter(theater_name=theatre_name).first()
        show = Show.objects.filter(show_name=show_name).first()
        movie_show = MovieTheatreShow.objects.filter(
             movie=movie, theatre=theatre, show=show).first()
        if movie_show:
            if movie_show.show.available_seats >= 1:
                movie_show.show.available_seats -= 1
                movie_show.show.save()
                return JsonResponse({"message": "You have successfully booked ticket for this show"})
            else:
                return JsonResponse({"message": "There are no Seats available for this Show"})
        else:
            return JsonResponse({"message": "Booking failed as the selected preferences are incorrect/in valid"})
    logging.warning("Unauthorized attempt to book ticket")
    return JsonResponse({"message": "Kindly login to continue booking for your favorite movie now"},
                        status=status.HTTP_401_UNAUTHORIZED)
