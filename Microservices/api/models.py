from django.db import models
from django.utils import timezone
from django.core.validators import DecimalValidator


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def as_json(self):
        return dict(username=self.username,
                    password=self.password
        )

    def __str__(self):
        return self.username
        #return '%s %s' % (self.username, self.password)


class Item(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[DecimalValidator])
    datePosted = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_json(self):
        return dict(item_id=str(self.pk),
                    name = self.name,
                    price = str(self.price),
                    datePosted = self.datePosted.isoformat(),
                    seller = self.seller.username)

    def __str__(self):
        return self.name

class Authenticator(models.Model):
    auth_num = models.CharField(max_length=3000)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    time_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.user, self.auth_num)

    def as_json(self):
        return dict(auth_num=self.auth_num,
                    user=self.user.username,
        )

class Recommendations(models.Model):
    item_id_num = models.IntegerField(primary_key=True)
    recommended_items = models.CharField(max_length=1000)
    def __str__(self):
        return '%s %s' % (self.item_id_num, self.recommended_items)

    def as_json(self):
        return dict(item_id=str(self.item_id_num), recommended_items=self.recommended_items)
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
