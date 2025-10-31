from django.forms import ModelForm
from .models import adoptionform

class adoption(ModelForm):
    class meta:
        model=adoptionform
        fields=['first_name','last_name','age','why_you_wanna_adopt','do_you_have_any_experince_before_with_animals']
