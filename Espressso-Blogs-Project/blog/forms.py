from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField( required=False, 
                                widget=forms.Textarea
                              )

class CommentForm(forms.ModelForm):
   # Django will introspect the model and build the corresponding form dynamically when using ModelForm. 
    class Meta:
        # indicate which model to build the form for
        model = Comment
        # explicitly tell Django which fields to include in the form
        fields = ['name', 'email', 'body']
    




