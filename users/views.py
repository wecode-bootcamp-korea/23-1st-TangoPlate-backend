import json, re, bcrypt, jwt
from reviews.models import Review

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Avg

from users.models         import User
from users.models         import WishList   
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
        
class WishListView(View):
    @login_decorator
    def get(self, request):
        user     = request.user
        results  = []
        wishlist = WishList.objects.filter(user_id=user.id)

        if not wishlist.exists():
            return JsonResponse({'MESSAGE':'NONE'}, status = 200)
        
        for wish in wishlist:
            restaurants = Restaurant.objects.filter(id=wish.restaurant_id)
            for restaurant in restaurants:
                results.append(
                    {
                        'name'        : restaurant.name,
                        'category'    : Category.objects.get(id=restaurant.category_id).name,
                        'location'    : Location.objects.get(id=restaurant.location_id).area,
                        "rating"      : restaurant.review_set.all().aggregate(Avg('rating')),
                        "review"      : [{
                        "images"      : [{"url" : image.image} for image in review.reviewimage_set.all()]
                    } for review in restaurant.review_set.all()]
                    }
                )
        return JsonResponse({'MESSAGE':results}, status=200)
