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

    # @property
    # def first_review(self):
    #     id = self.

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