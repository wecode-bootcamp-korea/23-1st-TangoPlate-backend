import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Avg

from users.models         import User
from users.models         import WishList   
from reviews.models       import Review
from restaurants.models   import Category, Location, Restaurant
from my_settings          import SECRET_KEY, const_algorithm
from users.utils          import login_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_ALREADY_EXIST"}, status=400)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            User.objects.create(
                nickname     =   data.get('nickname'),
                email        =   email,
                password     =   hashed_password.decode('UTF-8'),
                phone_number =   data['phone_number'],
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)      
            email    = data['email']
            password = data['password']        

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'INVALID_VALUE'}, status = 401)

            if bcrypt.checkpw(password.encode('utf-8'),User.objects.get(email=email).password.encode('utf-8')):
                nickname = User.objects.get(email = email).nickname
                token = jwt.encode({'id':User.objects.get(email=email).id}, SECRET_KEY, algorithm=const_algorithm)
            
                return JsonResponse({'TOKEN': token, "EMAIL":email, "NICKNAME":nickname}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class WishView(View):
    @login_decorator
    def delete(self, request, restaurant_id):
        try: 
            if WishList.objects.filter(user_id = request.user.id, restaurant_id=restaurant_id).exists():
                WishList.objects.filter(user_id = request.user.id, restaurant_id=restaurant_id).delete()
            return JsonResponse({'MESSAGE' : 'WISH_REMOVED'}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE' : "NOT_EXIST"}, status=404)
        
    @login_decorator
    def post(self, request, restaurant_id):
        try:             
            if not WishList.objects.filter(user_id = request.user.id, restaurant_id=restaurant_id).exists():
                WishList.objects.create(
                    user_id       = User.objects.get(id = request.user.id).id,
                    restaurant_id = Restaurant.objects.get(id = restaurant_id).id
                )
            return JsonResponse({'MESSAGE' : 'WISH_ADDED'}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE' : "NOT_EXIST"}, status=404)        
class WishListView(View):
    @login_decorator
    def get(self, request):
        user     = request.user
        wishlist = WishList.objects.filter(user_id=user.id)

        if not wishlist.exists():
            return JsonResponse({'MESSAGE':list()}, status = 404)
        
        results = [{
                'id'          : wish.restaurant.id,
                'name'        : wish.restaurant.name,
                'category'    : wish.restaurant.category.name,
                'location'    : wish.restaurant.location.area,
                "btn_toggle"  : False,
                "rating"      : wish.restaurant.review_set.all().aggregate(Avg('rating')),
                "images"      : wish.restaurant.review_set.filter(restaurant_id=wish.restaurant.id)[0].reviewimage_set.last().image,
            } for wish in wishlist ]
        return JsonResponse({'MESSAGE':results}, status=200)

