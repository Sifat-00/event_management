from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    location = models.CharField(max_length=200)


    date = models.DateField()


    time = models.TimeField()




    description = models.TextField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title

class Participant(models.Model):

    name = models.CharField(max_length=100)



    email = models.EmailField()


    events = models.ManyToManyField(Event,related_name='participants')

    def __str__(self):
        return self.name




class Profile(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)


    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_profile.png', blank=True)

    phone_num = models.CharField(max_length=20, blank=True)

    reset_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
