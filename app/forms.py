from django import forms
from .models import UserBio , Post , Comments

class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserBio
        fields = ['username' , 'bio' , 'img']

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control my-3' , 'id' : 'username' , 'placeholder' : ''}),
            'bio' : forms.TextInput(attrs={'class' : 'form-control my-3' , 'id' : 'bio' , 'placeholder' : ''}),
            'img' : forms.ClearableFileInput(attrs={'class' : 'form-control my-3'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['img' , 'caption']

        widgets = {
            'img' : forms.ClearableFileInput(attrs={'class' : 'form-control my-3 d-none' , 'id' : 'img'}),
            'caption' : forms.Textarea(attrs={'class' : 'form-control my-3' , 'id' : 'caption' , 'placeholder' : ''})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

        widgets = {
            'comment' : forms.TextInput(attrs={'class' : 'form-control my-3' , 'placeholder' : 'Add a comment'})
        }