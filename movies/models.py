from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=200)

    # class Meta:
    #     ordering = ('title',)

    def __str__(self):
        return f'{self.title} ({self.year})- directed by {self.director}'


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
