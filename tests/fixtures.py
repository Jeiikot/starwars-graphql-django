# Utils
from utils import constants

# Pytest
import pytest


@pytest.fixture
def graphql_url():
    return constants.GRAPHQL_PATH
