from django.contrib import admin
from .models import enterpets,adoptionform

class requestformadmin(admin.ModelAdmin):
    list_display=('first_name','last_name','age','why_you_wanna_adopt','do_you_have_any_experince_before_with_animals','reasons')
    list_filter=('status',)
    search_fields=['first_name','last_name']



admin.site.register(adoptionform,requestformadmin)
admin.site.register(enterpets)
# Register your models here.
