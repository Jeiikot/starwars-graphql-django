# Pytest
import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures("graphql_url")
class TestPlanetMutations:
    """
    Test class for Planet GraphQL mutations.
    """

    def test_create_planet(self, client, graphql_url):
        """
        Test creating a planet with minimal required data.

        Asserts:
            - The planet is created with the correct name.
            - No errors are returned in the response.
        """
        mutation = '''
        mutation {
          createPlanet(
            name: "Mustafar"
          ) {
            planet {
              id
              name
            }
          }
        }
        '''
        response = client.post(graphql_url, data={'query': mutation}, content_type='application/json')
        data = response.json()
        assert "errors" not in data
        assert data["data"]["createPlanet"]["planet"]["name"] == "Mustafar"
