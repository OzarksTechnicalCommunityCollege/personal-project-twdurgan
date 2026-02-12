from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

## Model managers here

class ViewableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status=Post.Status.DRAFT)

## Models here.

class Post(models.Model):
    # Drafts should not display to an end user browsing the site, where published images display normally and unapproved images display with a 'needs approval' notice.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        UNAPPROVED = 'UA', 'Unapproved'
        PUBLISHED = 'PB', 'Published'
    
    # The content ImageField is the most important field, make sure to pay attention to the arguments.
    # If I'm feeling ambitious, this might get changed to a FileField to allow for the upload of gifs, videos, and, in a better time, .swf files.
    content = models.ImageField(upload_to="booru\static\img")
    # All user-filled fields besides 'content' (and, potentially, 'tags') should be nullable if possible; anonymous users should be able to post but be severely rate-limited.
    # I've had problems trying to use id as the identifier for a post, particularly when calling __str__ for the model. Will think about solutions down the line.
    title = models.CharField(max_length=250, default="post")
    description = models.TextField(blank=True)
    altText = models.TextField(blank=True)
    # Individuals making posts are fielded as 'poster' because image content should primarily be attributed to an artist via tagging.
    # Posts are not deleted after user deletion; I want posts to remain after posters are gone, with only the actual author of an image able to delete said image externally.
    # Field is nullable, but I'm not sure if AUTH_USER_MODEL interferes with that ability.
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()
    viewable = ViewableManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def get_absolute_url(self):
        return reverse('booru:post_view', args=[self.id])

    def __str__(self):
        return self.title

# Figure out a way for a user to post either as their account or as an anonymous user with a text-entry name.
# Both the user and administration should be able to set a comment to inactive, but the user should not be able to reactivate it.
# This allows users to "delete" comments while still letting moderation take action on those with infringing contents, e.g. doxxing.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, blank=True)
    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        if self.name == '':
            return f'Comment by anonymous on {self.post}'
        else:
            return f'Comment by {self.name} on {self.post}'

# Keeping this and other tag-related code here for now; there are certain aspects of tagging that I want that TaggableManager might have a hard time with,
# but mirroring the structure that it uses shouldn't be impossible if I start to encounter problems, particularly with the creation of tag descriptions to be used on wiki-esque info pages.
# class Tag(models.Model):
#     tagName = models.CharField(max_length=250)
#     # Slugs are likely going to be required for ease-of-use in searching later down the line, if I had to hazard a guess.
#     # I would like searching via tags to require separation of tags and arguments only by spaces, e.g. "rhinoceros drinking-water resolution:>=100 order:resolution_descending"
#     # Low-priority: I would like tagSlugs to replace whitespace with underscores instead of dashes, as certain nouns that could be used for tagging might have dashes in them, and I find underscores are more readable.
#     tagSlug = models.SlugField(max_length=250)
#     tagType = models.CharField(max_length=50, default='General')
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.tagName

#     class Meta:
#         ordering = ['tagSlug']
#         indexes = [models.Index(fields=['tagSlug'])]

# Below here are some composite primary keys. They're for user favorites and a user blacklist, respectively.

class UserFavorites(models.Model):
    pk = models.CompositePrimaryKey("user", "post")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('booru.Post', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# Most composite keys are deleted on tag deletion, but I want blacklist tags to remain in the event of a tag being removed and later re-implemented.
# If people don't wanna see something, the absolute only way to accidentally put it on their page should be improper tagging of an image itself.
# class UserBlacklist(models.Model):
#     pk = models.CompositePrimaryKey("user", "tag")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     tag = models.ForeignKey('booru.Tag', on_delete=models.DO_NOTHING)