from django import forms
from .models import Comment

## Bound Fields

class CommentBoundField(forms.BoundField):
    comment_class = "comment"
    def css_classes(self, extra_classes=None):
        result = super().css_classes(extra_classes)
        if self.comment_class not in result:
            result += f" {self.comment_class}"
        return result.strip()
    
## Forms and ModelForms

# This and one other form will be created, once I have a better grasp on ModelForms.
# This one will be for mailing of a post to administration for the purposes of requesting image deletion or modification by the artist.
# It may also be used to request aliasing of an image to a higher-quality or artist-preferred version before deletion of the original.
class EmailPostForm(forms.Form):
    # No 'to' section, the emails from this will go to a static address.
    name = forms.CharField(label="Username", max_length=25, required=False)
    email = forms.EmailField(label="Your E-mail")
    subject = forms.CharField(max_length=50, required=True)
    request = forms.CharField(required=True, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    bound_field_class = CommentBoundField
    class Meta:
        model = Comment
        fields = ['name', 'body']

# TODO: A ModelForm should go here for the creation of posts, though I need to figure out how to change field labels for ModelForms.