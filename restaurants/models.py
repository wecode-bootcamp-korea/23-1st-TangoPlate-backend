from django.db    import models

class Restaurant(models.Model):
    name            = models.CharField(max_length=45)
    address         = models.CharField(max_length=100)
    phone_number    = models.CharField(max_length=50, null=True)
    location        = models.ForeignKey('Location',on_delete=models.CASCADE)
    category        = models.ForeignKey('Category', on_delete=models.CASCADE)
    serving_price   = models.ForeignKey('ServingPrice', on_delete=models.CASCADE)

    class Meta:
        db_table = 'restaurants'
    
    @property
    def latest_review(self):
        if not self.review_set.exists():
            return None

        return {
            "id"          : self.review_set.last().id,
            "user_id"     : self.review_set.last().user_id,
            "user_name"   : self.review_set.last().user_nickname,
            "description" : self.review_set.last().description,
            "image"       : self.review_set.last().reviewimage_set.last().image
        }

    @property
    def first_review(self):
        if not self.review_set.exists():
            return None

        return {
            "id"          : self.review_set.filter()[0].id,
            "user_id"     : self.review_set.filter()[0].user_id,
            "user_name"   : self.review_set.filter()[0].user.nickname,
            "description" : self.review_set.filter()[0].description,
            "image"       : self.review_set.filter()[0].reviewimage_set.last().image,
        }

class Menu(models.Model):
    restaurant     = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    item           = models.CharField(max_length=45)
    item_price     = models.DecimalField(max_digits= 10, decimal_places=0)

    class Meta:
        db_table = 'menus'

class Location(models.Model):
    area = models.CharField(max_length=45)

    class Meta:
        db_table = 'locations'

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class ServingPrice(models.Model):
    price = models.PositiveIntegerField()

    class Meta:
        db_table = 'serving_prices'