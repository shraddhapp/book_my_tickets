# book_my_tickets

A ticketting website where users can check the movies, cinemas, shows related information and book tickets


### Setting up the project

Requirement.txt is provided wih the project

to install all required dependencies please use -

```
'pip3 install -r requirements.txt' 
```

### APIs informtion and screenshots-

#### 1. Ability to view all the movies playing in your city

```
BaseIP/all-movies/<city_name>/  [GET]
```

![image](https://user-images.githubusercontent.com/80465706/143853540-fc0c3f35-e2a1-4aec-981a-f62f670f7da4.png)

#### 2. Ability to check all cinemas in which a movie is playing along with all the showtimes

```
BaseIP/all-shows/<movie_name>/  [GET]
```

![image](https://user-images.githubusercontent.com/80465706/143853315-1fa9ddad-4924-42ab-9ac9-7f3c7418207c.png)

#### 3. For each showtime, check the availability of seats
```
BaseIP/check-availability-for-showtime/ [GET]
```

![image](https://user-images.githubusercontent.com/80465706/143853174-27b8eeec-fb0d-43e8-8b1e-db827d7a06b7.png)


#### 4. User Sign up and login 
```
login [name='login']
logout [name='logout']
registration [name='registration'] [POST] -> {customer_name : username, pwd : password, city : city}
```

#### 5. Ability to book a ticket. (No payment gateway integration is required. Assume tickets can be booked for free)
```
book/<city_name>/<movie_name>/<theatre_name>/<show_name> [GET + PRIVATE]
```

![image](https://user-images.githubusercontent.com/80465706/143854428-afba1bb5-d6d6-4abf-ae35-68b9b05e16a1.png)




