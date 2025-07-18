import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from .types import CharacterNode, MovieNode, PlanetNode


class Query(graphene.ObjectType):
    character = relay.Node.Field(CharacterNode)
    all_characters = DjangoFilterConnectionField(CharacterNode)

    movie = relay.Node.Field(MovieNode)
    all_movies = DjangoFilterConnectionField(MovieNode)

    planet = relay.Node.Field(PlanetNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)
