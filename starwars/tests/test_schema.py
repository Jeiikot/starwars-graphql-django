# Graphene
from graphene.test import Client
from graphene.relay import Node

# Models
from starwars.models import Character, Movie

# Schema
from starwars.schema import schema

import pytest

@pytest.mark.django_db
class TestGraphQLMutations:
    def test_create_character_mutation(self):
        """
        Test creating a character with a movie.

        Asserts:
            - The character is created with the correct data.
            - The character is associated with the movie.
        """
        movie = Movie.objects.create(
            title="Test Movie",
            episode_id=1,
            opening_crawl="...",
            director="Lucas",
            producers="Lucas",
            release_date="1977-05-25",
        )
        global_id = Node.to_global_id("MovieNode", movie.id)

        mutation = '''
            mutation {
              createCharacter(name: "Luke Skywalker", species: "Human", birthYear: "19BBY", movies: ["%s"]) {
                character {
                  name
                  species
                  birthYear
                  movies { edges { node { title } } }
                }
              }
            }
        ''' % global_id
        client = Client(schema)
        executed = client.execute(mutation)

        assert executed["data"]["createCharacter"]["character"]["name"] == "Luke Skywalker"
        assert executed["data"]["createCharacter"]["character"]["movies"]["edges"][0]["node"]["title"] == "Test Movie"

    def test_list_characters_query(self):
        """
        Test listing all characters.

        Asserts:
            - The query returns a list of characters.
        """
        Character.objects.create(name="Leia Organa")
        client = Client(schema)
        query = '''
          query {
            allCharacters {
              edges {
                node {
                  name
                }
              }
            }
          }
        '''
        result = client.execute(query)
        assert "Leia Organa" in [edge["node"]["name"] for edge in result["data"]["allCharacters"]["edges"]]
