from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','thumbnail']

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','thumbnail']

    def save(self,commit=True):
        post=self.instance
        post.title=self.cleaned_data['title']
        post.content=self.cleaned_data['content']
        post.thumbnail=self.cleaned_data['thumbnail']

        if commit:
            post.save()
        return post