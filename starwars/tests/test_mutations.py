# Pytest
import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures("graphql_url")
class TestGraphQLMutations:
    """
    Test class for GraphQL mutations: createPlanet, createMovie, createCharacter.
    """

    def test_create_planet_success(self, client, graphql_url):
        """
        Test creating a planet with required data only.

        Asserts:
            - The planet is created successfully.
            - No errors are returned.
            - The returned planet's "name" field matches the expected value.
        """
        mutation = '''
        mutation {
          createPlanet(
            name: "Mustafar"
          ) {
            planet {
              id
              name
              climate
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert response.status_code == 200
        assert "errors" not in data
        assert data["data"]["createPlanet"]["planet"]["name"] == "Mustafar"

    def test_create_movie_success(self, client, graphql_url):
        """
        Test creating a movie with all required fields.

        Asserts:
            - The movie is created successfully with correct data.
            - No errors are returned.
            - The returned movie's "title" and "director" fields match the expected values.
        """
        mutation = '''
        mutation {
          createMovie(
            title: "The Mandalorian",
            episodeId: 10,
            director: "Jon Favreau",
            producers: "Dave Filoni, Jon Favreau",
            releaseDate: "2023-12-12"
          ) {
            movie {
              id
              title
              director
              releaseDate
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert response.status_code == 200
        assert "errors" not in data
        assert data["data"]["createMovie"]["movie"]["title"] == "The Mandalorian"
        assert data["data"]["createMovie"]["movie"]["director"] == "Jon Favreau"

    def test_create_movie_invalid_date(self, client, graphql_url):
        """
        Test creating a movie with an invalid date format.

        Asserts:
            - The mutation returns an error due to invalid date format.
        """
        mutation = '''
        mutation {
          createMovie(
            title: "Bad Date Movie",
            episodeId: 999,
            director: "No One",
            producers: "None",
            releaseDate: "12-31-2020"
          ) {
            movie {
              id
              title
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert response.status_code == 400

    def test_create_character_success(self, client, graphql_url):
        """
        Test creating a character with required data only.

        Asserts:
            - The character is created successfully.
            - No errors are returned.
            - The returned character's "name" field matches the expected value.
        """
        mutation = '''
        mutation {
          createCharacter(
            name: "Grogu"
          ) {
            character {
              id
              name
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert response.status_code == 200
        assert "errors" not in data
        assert data["data"]["createCharacter"]["character"]["name"] == "Grogu"

    def test_create_character_with_invalid_movie(self, client, graphql_url):
        """
        Test creating a character with an invalid movie ID.

        Asserts:
            - The mutation returns an error due to invalid movie ID.
            - No errors are returned.
        """
        mutation = '''
        mutation {
          createCharacter(
            name: "Test Character",
            movies: ["SW_WRONG_ID"]
          ) {
            character {
              id
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert response.status_code == 200
        assert "errors" in data
