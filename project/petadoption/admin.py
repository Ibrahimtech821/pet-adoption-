from django.contrib import admin
from .models import enterpets,adoptionform

class requestformadmin(admin.ModelAdmin):
    list_display=('get_user','get_pet','age','why_you_wanna_adopt','do_you_have_any_experince_before_with_animals','reasons')
    list_filter=('status',)
    list_search=('user__username','pet__pet_name')
    def get_user(self,obj):
        return obj.user.username if obj.user else '-'
    get_user.short_description='user'
    def get_pet(self,obj):
        return obj.pet.pet_name if obj.pet else '-'
    get_pet.short_description='pet'  
    def save_model(self,request,obj,form,change):
       
        super().save_model(request,obj,form,change)
        pet=obj.pet
        if obj.status=='accepted':
            pet.is_adopted=True
        else:
            pet.is_adopted=False
        pet.save() 

admin.site.register(adoptionform,requestformadmin)
admin.site.register(enterpets)
# Register your models here.
