from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #HTML <input type="text>
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # form is created automatically by Django after analyzing a given model
        fields = ['name', 'email', 'body'] # three columns are taken into account 


class SearchForm(forms.Form):
    query = forms.CharField()