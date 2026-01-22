from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils import timezone

# Model managers here

class ViewableManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=(Post.Status.PUBLISHED or Post.Status.UNAPPROVED)))

# Models here.

class Post(models.Model):
    # Drafts should not display to an end user browsing the site, where published images display normally and unapproved images display with a 'needs approval' notice.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        UNAPPROVED = 'UA', 'Unapproved'
        PUBLISHED = 'PB', 'Published'

    # All user-filled fields besides 'content' (and, potentially, 'tags') should be nullable if possible; anonymous users should be able to post but be severely rate-limited.
    # I've had problems trying to use id as the identifier for a post, particularly when calling __str__ for the model. Will think about solutions down the line.
    title = models.CharField(max_length=250, default="post")
    # Make sure to add arguments to ImageField when fields are more well-understood.
    description = models.TextField(blank=True, null=True)
    # Individuals making posts are fielded as 'poster' because image content should primarily be attributed to an artist via tagging.
    # Posts are not deleted after user deletion; I want posts to remain after posters are gone, with only the actual author of an image able to delete said image externally.
    # Field is nullable, but I'm not sure if AUTH_USER_MODEL interferes with that ability.
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    content = models.ImageField()
    # # A list of tags for the post should go below here, potentially. I want to figure out a many-to-one relationship so many posts can reference a single tag (or multiple tags for that matter)
    # # A single tag should be able to occupy multiple posts as well, obviously. I'm also exploring the usage of composite keys below my models as a method of tagging.
    # tags = models.JSONField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()
    viewable = ViewableManager()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
    
class Tag(models.Model):
    tagName = models.CharField(max_length=250)
    # Slugs are likely going to be required for ease-of-use in searching later down the line, if I had to hazard a guess.
    # I would like searching via tags to require separation of tags and arguments only by spaces, e.g. "rhinoceros drinking-water resolution:>=100 order:resolution_descending"
    tagSlug = models.SlugField(max_length=250)
    tagType = models.CharField(max_length=50, default='General')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tagName

    class Meta:
        ordering = ['tagSlug']
        indexes = [models.Index(fields=['tagSlug'])]

# Below here are some composite primary keys. The first is a potential route for tag-image relationships, the second is for user favorites, and the third is for a user blacklist.

class PostTags(models.Model):
    pk = models.CompositePrimaryKey("image", "tag")
    image = models.ForeignKey('booru.Post', on_delete=models.CASCADE)
    tag = models.ForeignKey('booru.Tag', on_delete=models.CASCADE)

class UserFavorites(models.Model):
    pk = models.CompositePrimaryKey("user", "post")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('booru.Post', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# Most composite keys are deleted on tag deletion, but I want blacklist tags to remain in the event of a tag being removed and later re-implemented.
# If people don't wanna see something, the absolute only way to accidentally put it on their page should be improper tagging of an image itself.
class UserBlacklist(models.Model):
    pk = models.CompositePrimaryKey("user", "tag")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey('booru.Tag', on_delete=models.DO_NOTHING)