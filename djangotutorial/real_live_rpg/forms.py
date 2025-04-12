from django import forms
from django.utils import timezone
from .models import TimeSpent, Skill

#   
class TimeSpentForm(forms.ModelForm):
    class Meta:
        model = TimeSpent 
        fields = ['skill', 'date', 'start_time', 'end_time']
        #
        widgets = {
            'skill': forms.Select(attrs={
                'class':'form-select'
            }), 
            'date': forms.DateInput(attrs={
                "class":"form-control",
                'type':'date'                
                }),
            'start_time': forms.TimeInput(attrs={
                "class":"form-control",
                'type': 'time'
                }),
            'end_time': forms.TimeInput(attrs={
                "class":"form-control",
                'type': 'time'
                }),
        }
    #
    def __init__(self, *args, **kwargs):
        # 
        super().__init__(*args, **kwargs)
        #
        today = timezone.localdate()
        self.fields["date"].initial = today 
        

#
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill 
        fields = ["skill_name"]
        #
        widgets = {
            'skill_name': forms.TextInput(attrs={
                'class':'form-control',
                "type":"text"
            }), 
        }
    #
    def __init__(self, *args, **kwargs):
        #
        super().__init__(*args, **kwargs)

#
