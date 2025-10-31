from django.db import models

choice={

    'Yes':'yes',
    'No':'no'

}


# Create your models here.
class enterpets(models.Model):
    pets={
    'Dog':'dog',
    'Cat':'cat',
    'turtle':'turtle',
    'bird':'bird',
}
    pet_name=models.CharField(max_length=255)
    Age=models.IntegerField(choices=pets,default="unkown")
    specie=models.CharField(choices=pets,max_length=100,default='dog')
    description=models.CharField(max_length=1000)
    any_injuries=models.CharField(choices=choice,max_length=4,default='No')
    describe_if_of_injury_if_there=models.CharField(max_length=255) 

class adoptionform(models.Model):
    statu={
        'pending':'pending',
        'accepted':'accepted',
        'reject':'reject'

    }
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    age=models.IntegerField()
    why_you_wanna_adopt=models.CharField(max_length=1000)
    do_you_have_any_experince_before_with_animals=models.CharField(choices=choice,max_length=100,default='Yes')
    status=models.CharField(choices=statu,max_length=100,default='pending')


