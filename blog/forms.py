from django import forms
from .models import Post,Comment
from mptt.forms import TreeNodeChoiceField


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


class CommentForm(forms.ModelForm):
    parent=TreeNodeChoiceField(queryset=Comment.objects.all())

    # TODO we have to remove required parent field
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # THis for removing the selected option box from comment form
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['name', 'parent', 'email', 'content']