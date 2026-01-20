from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    # Drafts should not display to an end user browsing the site, where published images display normally and unapproved images display with a 'needs approval' notice.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        UNAPPROVED = 'UA', 'Unapproved'
        PUBLISHED = 'PB', 'Published'

    # All fields besides 'content' and 'tags' should be nullable; anonymous users should be able to post but be severely rate-limited.
    title = models.CharField(max_length=250)
    # Make sure to add arguments to ImageField when fields are more well-understood.
    description = models.TextField()
    # Individuals making posts are fielded as 'poster' because image content should primarily be attributed to an artist via tagging.
    # Change 'CASCADE' later in production; I want posts to remain after posters are gone, with only the actual author of an image able to submit deletion requests.
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ImageField()
    # A list of tags for the post should go here, potentially. I want to figure out a many-to-one relationship so many posts can reference a single tag (or multiple tags for that matter)
    # A single tag should be able to occupy multiple posts as well, obviously.
    tags = models.JSONField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    

    def __str__(self):
        return self.id
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
    
class Tag(models.Model):
    tagName = models.CharField(max_length=250)
    # Slugs are likely going to be required for ease-of-use in searching later down the line, if I had to hazard a guess.
    # I would like searching via tags to require separation of tags and arguments only by spaces, e.g. "rhinoceros drinking-water resolution:>=100 order:resolution_descending"
    tagSlug = models.SlugField(max_length=250)
    description = models.TextField()

    class Meta:
        ordering = ['tagSlug']
        indexes = [models.Index(fields=['tagSlug'])]