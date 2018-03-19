from django.db import models
from django.utils import timezone
from django.core.validators import DecimalValidator

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username
        #return '%s %s' % (self.username, self.password)
'''
    def create(self, username, password):
        self.username = username
        self.password = password
        self.save()
'''

class Item(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[DecimalValidator])
    datePosted = models.DateTimeField(default=timezone.now())
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_json(self):
        return dict(item_id=str(self.pk),
                    name = self.name,
                    price = str(self.price),
                    datePosted = self.datePosted.isoformat(),
                    seller = self.seller.username)

    def __str__(self):
        return self.name

'''
    def post(self, name, username, price):
        self.datePosted = timezone.now()
        self.name = name
        self.seller = username
        self.price = price
        self.save()
'''

'''
FOR FUTURE IMPLEMENTATION
class Review(models.Model):
    user = models.CharField(max_length=200)
    itemID = models.IntegerField()
    reviewTitle = models.CharField(max_length=200)
    reviewBody = models.TextField()
    datePosted = models.DateTimeField(auto_now_add=True)

    def post(self, user, item, title, body):
        self.datePosted = timezone.now()
        self.user = user
        self.itemID = item.id
        self.reviewTitle = title
        self.reviewBody = body
        self.save()

    def __str__(self):
        return self.reviewTitle
'''