# Django
from django.db import models

# Externals
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Planet(BaseModel):
    # Fields
    swapi_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    climate = models.CharField(max_length=100, blank=True)
    terrain = models.CharField(max_length=100, blank=True)
    rotation_period = models.CharField(max_length=10, blank=True)
    orbital_period = models.CharField(max_length=10, blank=True)
    diameter = models.CharField(max_length=10, blank=True)
    gravity = models.CharField(max_length=50, blank=True)
    surface_water = models.CharField(max_length=10, blank=True)
    population = models.CharField(max_length=20, blank=True)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['swapi_id'],
                name='unique_swapi_id_not_null_in_planet',
                condition=~models.Q(swapi_id=None),
            ),
        ]
    def __str__(self):
        return self.name


class Movie(BaseModel):
    # Fields
    swapi_id = models.IntegerField(null=True)
    title = models.CharField(max_length=100)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=100)
    producers = models.CharField(max_length=255)

    # Data Fields
    release_date = models.DateField()

    # M2M Fields
    planets = models.ManyToManyField(Planet, related_name="movies")

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['swapi_id'],
                name='unique_swapi_id_not_null_in_movie',
                condition=~models.Q(swapi_id=None),
            ),
        ]

    def __str__(self):
        return self.title


class Character(BaseModel):
    # Fields
    swapi_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    birth_year = models.CharField(max_length=10, blank=True)
    species = models.CharField(max_length=50, blank=True)
    height = models.CharField(max_length=10, blank=True)
    mass = models.CharField(max_length=10, blank=True)
    hair_color = models.CharField(max_length=50, blank=True)
    skin_color = models.CharField(max_length=50, blank=True)
    eye_color = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    homeworld = models.ForeignKey(
        Planet, null=True, blank=True, on_delete=models.SET_NULL, related_name="residents"
    )

    # M2M Fields
    movies = models.ManyToManyField(Movie, related_name="characters")

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['swapi_id'],
                name='unique_swapi_id_not_null_in_character',
                condition=~models.Q(swapi_id=None),
            ),
        ]

    def __str__(self):
        return self.name
