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
    ('Turtle','turtle'),
    ('Bird','bird'),
    ('Rabbit','rabbit')
]
    pet_name=models.CharField(max_length=255)
    Age = models.IntegerField(default=0)
    specie=models.CharField(choices=pets,max_length=100,default='dog')
    description=models.CharField(max_length=1000 , default=' ')
    breed = models.CharField(max_length=100, default='Unknown')  
    color = models.CharField(max_length=50, default='Unknown') 
    any_injuries=models.CharField(choices=choice,max_length=4,default='no')
    describe_if_of_injury_if_there=models.CharField(max_length=255 , default=' ') 
    image=models.URLField(max_length=500,blank=True,null=True)
    is_adopted=models.BooleanField(default=False)
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
    

class PetFood(models.Model):
    FOOD_TYPE_CHOICES = [
        ('dry', 'Dry Food'),
        ('wet', 'Wet Food'),
        ('treat', 'Treat'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)
    suitable_for = models.CharField(max_length=50)  # e.g. "Adult Dogs"
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='petfood/', blank=True, null=True)

    def __str__(self):
        return self.name
    
