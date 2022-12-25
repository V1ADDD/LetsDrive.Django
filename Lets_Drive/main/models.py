import datetime

from django.db import models


class Auto(models.Model):
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=100)
    fuel = models.CharField(max_length=15)
    fueled = models.IntegerField()
    probeg = models.IntegerField()
    korobka = models.CharField(max_length=15)
    available = models.BooleanField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return str(self.id) + ". " + self.name


class Users(models.Model):
    fio = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    photo_pass = models.ImageField(upload_to='images_pass')
    photo_vu = models.ImageField(upload_to='images_vu')
    age = models.IntegerField()
    staz = models.IntegerField()
    available = models.BooleanField()

    def __str__(self):
        return str(self.id) + ". " + self.fio


class Drives(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    distance = models.FloatField()
    time_start = models.DateTimeField()
    time_finish = models.DateTimeField()
    price = models.FloatField()

    class Meta:
        ordering = ["-time_start"]

    def __str__(self):

        return str(self.time_start.date())+" "+str(self.time_start.time())

    def time(self):
        return self.time_finish - self.time_start


BREAK_STATUS = (
    ('на рассмотрении', 'WAITLIST'),
    ('зарегистрирована', 'REGISTERED'),
    ('исправлена', 'FIXED'),
    ('отклонена', 'DECLINED')
)


class Breaks(models.Model):
    drive = models.ForeignKey(Drives, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='breaks')
    status = models.CharField(max_length=20, choices=BREAK_STATUS)

    def __str__(self):
        return str(self.id)+" - "+self.status


class Tarify(models.Model):
    name = models.CharField(max_length=50)
    price_km = models.FloatField()
    price_minute = models.FloatField()
    time_limit = models.FloatField()
    distance_limit = models.FloatField()
    price = models.FloatField()
    available = models.BooleanField()

    def __str__(self):
        return str(self.name)
