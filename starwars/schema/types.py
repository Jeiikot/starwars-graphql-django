# Graphene
from graphene_django import DjangoObjectType
from graphene import relay

# Models
from starwars.models import Planet, Movie, Character


class PlanetNode(DjangoObjectType):
    class Meta:
        model = Planet
        interfaces = (relay.Node,)
        filter_fields = ['name']


class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        interfaces = (relay.Node,)
        filter_fields = ['title', 'director']


class CharacterNode(DjangoObjectType):
    class Meta:
        model = Character
        interfaces = (relay.Node,)
        filter_fields = ['name']
