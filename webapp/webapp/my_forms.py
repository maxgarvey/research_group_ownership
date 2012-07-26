'''/webapp/webapp/my_forms.py'''
from django import forms

#the form we need here
class GroupOwnershipForm(forms.Form):
    groupname = forms.CharField(max_length=100)
