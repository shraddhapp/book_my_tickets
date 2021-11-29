from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('all-movies/<city_name>/', get_all_movies_in_city),
    path('all-shows/<movie_name>/', get_cinema_and_show_details_for_movie),
    path('check-availability-for-showtime/',get_availability_for_all_shows),
    path('book/<city_name>/<movie_name>/<theatre_name>/<show_name>', book_ticket, name="book_ticket"),
    path('api-auth/', include('rest_framework.urls')),
    url('login', user_login, name="login"),
    url('logout', user_logout, name="logout"),
    url('registration', customer_signup, name="registration"),
]
