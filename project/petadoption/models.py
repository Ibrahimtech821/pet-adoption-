from django.db import models

choice={

    'Yes':'yrs',
    'No':'no'

}

# Create your models here.
class enterpets(models.Model):
    pet_name=models.CharField(max_length=255)
    Age=models.IntegerField(max_length=100)
    description=models.CharField(max_length=1000)
    any_injuries=models.CharField(choices=choice,max_length=4,default='No')
    describe_if_of_injury_if_there=models.CharField(max_length=255) 

