from django import forms
from .models import BusPass, Route

# Form for applying bus pass
class BusPassApplyForm(forms.ModelForm):
    class Meta:
        model = BusPass
        fields = ['student', 'route']

# Form for adding/editing routes
class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'
