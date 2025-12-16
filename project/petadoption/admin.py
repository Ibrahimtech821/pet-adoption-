from django.contrib import admin
from .models import enterpets,adoptionform,PetFood
from django.core.mail import send_mail
from django.conf import settings

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
        user=obj.user
        if obj.status=='accepted':
            pet.is_adopted=True
            subject="Adoption Application Accepted!!❤️"
            message=f"Dear {user.username},\n\nCongratulations! Your adoption application for {pet.pet_name} has been accepted. We are thrilled to inform you that you can now welcome {pet.pet_name} into your home.\n\nPlease contact us at your earliest convenience to discuss the next steps and arrange for the adoption process.\n\nThank you for choosing to adopt and provide a loving home for our furry friends!\n\nBest regards,\nPet Adoption Team"
        elif obj.status=='reject':
            pet.is_adopted=False
            subject='Adoption Application rejected!💔'
            message=f"Dear {user.username},\n\nWe regret to inform you that your adoption application for {pet.pet_name} has been rejected. We understand that this news may be disappointing, and we want to assure you that the decision was made after careful consideration.\n\nIf you have any questions or would like feedback on your application, please feel free to reach out to us. We appreciate your interest in adopting and encourage you to consider applying again in the future.\n\nThank you for your understanding.\n\nBest regards,\nPet Adoption Team"
        else:
            pet.is_adopted = False
            subject = message = None

        pet.save() 

        if subject and message:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        


admin.site.register(adoptionform,requestformadmin)
admin.site.register(enterpets)

@admin.register(PetFood)
class PetFoodAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'food_type', 'suitable_for')
    list_filter = ('food_type', 'brand_name')
    search_fields = ('brand_name','suitable_for')

# Register your models here.
