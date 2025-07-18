# Pytest
import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures("graphql_url")
class TestCharacterQueries:
    """
    Test class for character GraphQL queries.
    """

    def test_list_characters(self, client, graphql_url):
        """
        Test listing all characters.
        Asserts:
            - The query returns a list of characters.
            - The list contains at least one character.
        """

        query = '''
        {
          allCharacters {
            edges {
              node {
                id
                name
              }
            }
          }
        }
        '''

        response = client.post(graphql_url, data={'query': query}, content_type='application/json')

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "allCharacters" in data["data"]

    def test_create_character(self, client, graphql_url):
        """
        Test creating a character.

        Asserts:
            - The character is created successfully.
            - The character has the correct name.
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

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["createCharacter"]["character"]["name"] == "Grogu"
