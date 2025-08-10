from django.db import models


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
