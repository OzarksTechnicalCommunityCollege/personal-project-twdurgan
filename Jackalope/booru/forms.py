from django import forms

# This and one other form will be created, once I have a better grasp on ModelForms.
# This one will be for mailing of a post to administration for the purposes of requesting image deletion by the artist.
# It may also be used to request aliasing of an image to a higher-quality or artist-preferred version before post deletion of the original.
class EmailPostForm(forms.Form):
    # No 'to' section, the emails from this will go to a static address.
    name = forms.CharField(label="Username", max_length=25, required=False)
    email = forms.EmailField(label="Your E-mail")
    subject = forms.CharField(max_length=50, required=True)
    request = forms.CharField(required=True, widget=forms.Textarea)