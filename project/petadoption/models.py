from django.conf import settings
from django.db import models

choice=[

    ('yes','Yes'),
    ('no','No')

]


# Create your models here.
class enterpets(models.Model):
    pets=[
    ('Dog','dog'),
    ('Cat','cat'),
    ('turtle','turtle'),
    ('bird','bird'),
]
    pet_name=models.CharField(max_length=255)
    Age = models.IntegerField(default=0)
    specie=models.CharField(choices=pets,max_length=100,default='dog')
    description=models.CharField(max_length=1000)
    breed = models.CharField(max_length=100, default='Unknown')  
    color = models.CharField(max_length=50, default='Unknown') 
    any_injuries=models.CharField(choices=choice,max_length=4,default='no')
    describe_if_of_injury_if_there=models.CharField(max_length=255) 

    def __str__(self):
        return self.pet_name + '' + self.breed 

class adoptionform(models.Model):
    statu=[
        ('pending','pending'),
        ('accepted','accepted'),
        ('reject','reject')

    ]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='adoption_requests')
    pet=models.ForeignKey('enterpets',null=True,blank=True,on_delete=models.SET_NULL,related_name='adoption_requests')
    age=models.IntegerField()
    why_you_wanna_adopt=models.CharField(max_length=1000)
    do_you_have_any_experince_before_with_animals=models.CharField(choices=choice,max_length=100,default='Yes')
    status=models.CharField(choices=statu,max_length=100,default='pending')
    reasons=models.CharField(max_length=1200,default='no reason provided')
    def __str__(self):
        return self.user.username + '' + self.pet.pet_name

