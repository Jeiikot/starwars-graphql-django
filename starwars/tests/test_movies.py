# Pytest
import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures("graphql_url")
class TestMovieMutations:
    """
    Test class for Movie GraphQL mutations.
    """

    def test_create_movie_success(self, client, graphql_url):
        """
        Test creating a movie with all required fields.

        Asserts:
            - The movie is created successfully with correct data.
            - No errors are returned.
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
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert "errors" not in data
        assert data["data"]["createMovie"]["movie"]["title"] == "The Mandalorian"

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
        assert "errors" in data
