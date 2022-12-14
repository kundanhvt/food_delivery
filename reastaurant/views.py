from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import Restaurant, Image, Food, Cart, Order
from user.models import users
import logging
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from user.models import Address
import geopy.distance


def restaurant(request, id):
    try:
        restaurent = Restaurant.objects.get(id=id)
        return render(request, "restaurant.html",context= {"restaurant": restaurent, "foods":""})
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

def restaurants(request):
    try:
        geolocator = Nominatim(user_agent="kundan")
        latitude = request.session.get('latitude',None)
        longitude = request.session.get('longitude',None)
        restaurants = None
        if latitude == None or longitude == None:
            restaurants = Restaurant.objects.all().order_by('id')
        else:
            print(latitude)
            print(longitude)
            location = geolocator.reverse(latitude+","+longitude)
            address = location.raw['address']
            city = None
            state = None
            if 'city' not in address.keys() and 'state' not in address.keys():
                restaurants = Restaurant.objects.all().order_by('id')
            elif 'city' not in address.keys():
                state = address['state']
                print('restaurant all')
                add = Address.objects.filter(state__iexact=state).values_list('id')
                restaurants = Restaurant.objects.filter(address__id__in=add).order_by('id')
            elif 'state' not in address.keys():
                city = address['city']
                print('restaurant all')
                add = Address.objects.filter(city__iexact=city).values_list('id')
                restaurants = Restaurant.objects.filter(address__id__in=add).order_by('id')
            else:
                city = address['city']
                state = address['state']
                print(city)
                print(state)
                print('restaurant all')
                add = Address.objects.filter(city__iexact=city,state__iexact=state).values_list('id')
                restaurants = Restaurant.objects.filter(address__id__in=add).order_by('id')
        paginator = Paginator(restaurants, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'restaurants.html',context={"page_obj":page_obj})
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

@login_required(login_url='user:login')
def cart(request):
    try:
        carts = request.user.all_cart_food.all()
        total=0
        for cart in carts:
            total += cart.quantity * cart.food.price
        return render(request, "cart.html", context={"carts":carts,"total_price":total})
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

@login_required(login_url='user:login')
def add_to_cart(request, res_id, food_id):
    try:
        carts = request.user.all_cart_food.all()
        if(len(carts)==0):
            restaurant = Restaurant.objects.get(id=res_id)
            food = Food.objects.get(id=food_id)
            cart = Cart(food=food, quantity = 1,user=request.user, restaurant = restaurant)
            cart.save()
        else:
            res = carts[0].restaurant.id
            if int(res) != int(res_id):
                carts = request.user.all_cart_food.all()
                total=0
                for cart in carts:
                    total += cart.quantity * cart.food.price
                return render(request, "cart.html", context={"carts":carts,"total_price":total,"cart_is_full":True})
            else:
                for cart in carts:
                    if int(cart.food.id) == int(food_id):
                        cart.quantity = cart.quantity+1
                        cart.save()
                        return redirect(reverse('reastaurent:cart'))
                food = Food.objects.get(id=food_id)
                cart = Cart(food=food,quantity=1,user = request.user, restaurant =carts[0].restaurant)
                cart.save()
                print(cart)
        return redirect(reverse('reastaurent:cart'))
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')


@login_required(login_url='user:login')
def decrement_quantity(request,cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        if cart.quantity == 1:
            pass
        else:
            cart.quantity -=1
            cart.save()
        return redirect(reverse('reastaurent:cart'))
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

@login_required(login_url='user:login')
def increment_quantity(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.quantity +=1
        cart.save()
        return redirect(reverse('reastaurent:cart'))
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

@login_required(login_url='user:login')
def delete_cart(request):
    try:
        id = request.GET.get('id')
        cart = Cart.objects.get(id=id)
        cart.delete()
        return redirect(reverse('reastaurent:cart'))
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')


@login_required(login_url='user:login')
def delete_all_cart(request):
    try:
        carts = request.user.all_cart_food.all()
        for cart in carts:
            cart.delete()
        return redirect(reverse('reastaurent:restaurant_all'))
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')


def food(request,id):
    try:
        food = Food.objects.get(id=id)
        return render(request, 'food.html',context={"food":food})
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

def view_all_food(request):
    try:
        foods = Food.objects.all().order_by('id')
        paginator = Paginator(foods, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'foods.html',context={"page_obj":page_obj})
    except Exception as ex:
        logging.warning(ex)
        return render(request,'error.html')

@login_required
def shipping(request):
    carts = request.user.all_cart_food.all()
    subtotal=0
    resadd = carts[0].restaurant.address
    coords_1 = None
    coords_2 = None
    if resadd.latitude == None or resadd.longitude == None:
        city = resadd.city
        state = resadd.state
        geolocator = Nominatim(user_agent="kundan")
        location = geolocator.geocode(city+' '+state)
        resadd.latitude = location.latitude
        resadd.longitude = location.longitude
        resadd.save()
        coords_1 = (location.latitude, location.longitude)
    else:
        coords_1 = (resadd.latitude, resadd.longitude)


    if request.user.address.latitude == None or request.user.address.longitude == None:
        city = request.user.address.city
        state = request.user.address.state
        ulocation = geolocator.geocode(city+' '+state)
        request.user.address.latitude = ulocation.latitude
        request.user.address.longitude = ulocation.longitude
        request.user.address.save()
        coords_2 = (ulocation.latitude, ulocation.longitude)
    else:
        coords_2 = (request.user.address.latitude, request.user.address.longitude)

    distance = geopy.distance.geodesic(coords_1, coords_2).km
    for cart in carts:
        subtotal += cart.quantity * cart.food.price


    shipping=int(distance * 50)
    total = subtotal+shipping
    if request.method == 'POST':
        data = request.POST.get('payment')
        order = Order(price = total,user=request.user,payment=data)
        order.save()
        carts = request.user.all_cart_food.all()
        for cart in carts:
            cart.delete()
        return HttpResponse('success')
    return render(request,'shipping.html',context={'subtotal':subtotal,'shipping':shipping,'total':total})


def search(request):
    item = []
    if request.method == 'POST':
        data = request.POST.get('search').lower()
        restaurants = Restaurant.objects.filter(name__icontains=data)
        foods = Food.objects.filter(name__icontains=data)

        for res in restaurants:
            item.append(['rastaurant',res])
        
        for food in foods:
            item.append(['food',food])
    return render(request,'search_result.html',context={"page_obj":item})