from django.db import models
import datetime 
# from django.utils import timezone
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    add_users = models.BooleanField()
    give_access = models.BooleanField()

    def __str__(self):
        return self.fullname
    
class Client_details(models.Model):
    client_name = models.CharField(max_length=50)
    building_name = models.CharField(max_length=50)
    flat_no = models.CharField(max_length=50)

    def __str__(self):
        return self.client_name + " " + self.building_name

class glass(models.Model):
    client = models.ForeignKey(Client_details, db_column='client', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50)
    glass_name = models.CharField(max_length=50)
    glassSize1 = models.CharField(max_length=50)
    glassSize2 = models.CharField(max_length=50)
    polish = models.CharField(max_length=20, default = 0)
    

    
