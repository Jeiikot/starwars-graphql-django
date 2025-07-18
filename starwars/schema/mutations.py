# Graphene
from graphene import String, List, Field, relay
import graphene

# Models
from starwars.models import Planet, Movie, Character

# Schema
from starwars.schema.types import CharacterNode, PlanetNode, MovieNode

# Utils
from datetime import datetime


class CreatePlanet(graphene.Mutation):
    """
    Mutation to create a new planet in the Star Wars universe.

    Args:
        - name (str): Name of the planet (required).
        - climate (str, optional): Climate description.
        - terrain (str, optional): Terrain type.
        - rotation_period (str, optional): Rotation period.
        - orbital_period (str, optional): Orbital period.
        - diameter (str, optional): Diameter.
        - gravity (str, optional): Gravity.
        - surface_water (str, optional): Surface water.
        - population (str, optional): Population.

    Returns:
        - planet (PlanetNode): The created planet object.
    """
    class Arguments:
        name = String(required=True)
        climate = String()
        terrain = String()
        rotation_period = String()
        orbital_period = String()
        diameter = String()
        gravity = String()
        surface_water = String()
        population = String()

    planet = Field(PlanetNode)

    def mutate(self, info, name, climate=None, terrain=None, rotation_period=None, orbital_period=None,
               diameter=None, gravity=None, surface_water=None, population=None):
        fields = dict(
            name=name,
            climate=climate or '',
            terrain=terrain or '',
            rotation_period=rotation_period or '',
            orbital_period=orbital_period or '',
            diameter=diameter or '',
            gravity=gravity or '',
            surface_water=surface_water or '',
            population=population or ''
        )

        # Create Planet
        planet = Planet(**fields)
        planet.save()

        return CreatePlanet(planet=planet)


class CreateMovie(graphene.Mutation):
    """
    Mutation to create a new movie (film) in the Star Wars universe.

    Args:
       - title (str): Movie title (required).
       - episode_id (int): Episode number (required).
       - opening_crawl (str, optional): Opening crawl text.
       - director (str): Director's name (required).
       - producers (str): Producers (required).
       - release_date (str): Release date in YYYY-MM-DD format (required).
       - planets (list of ID, optional): List of planet Relay global IDs to associate.

    Returns:
       - movie (MovieNode): The created movie object.

    Raises:
        - Exception: If one or more Planet IDs are invalid.
    """
    class Arguments:
        title = String(required=True)
        episode_id = graphene.Int(required=True)
        opening_crawl = String()
        director = String(required=True)
        producers = String(required=True)
        planets = List(graphene.ID)
        release_date = String(required=True)

    movie = Field(MovieNode)

    def mutate(self, info, title, episode_id, opening_crawl=None, director=None, producers=None,
               planets=None, release_date=None):
        try:
            release_date_parsed = datetime.strptime(release_date, "%Y-%m-%d").date()
        except Exception:
            raise Exception("release_date must be in format YYYY-MM-DD")

        movie = Movie(
            title=title,
            episode_id=episode_id,
            opening_crawl=opening_crawl or '',
            director=director,
            producers=producers,
            release_date=release_date_parsed,
        )
        movie.save()

        # Add Planets
        if planets:
            planet_instances = [
                relay.Node.get_node_from_global_id(info, pid, only_type=PlanetNode)
                for pid in planets
            ]

            if None in planet_instances:
                raise Exception("One or more Planet IDs are invalid")

            movie.planets.set(planet_instances)

        return CreateMovie(movie=movie)


class CreateCharacter(graphene.Mutation):
    """
    Mutation to create a new character in the Star Wars universe.

    Args:
       - name (str): Character name (required).
       - species (str, optional): Species of the character.
       - birth_year (str, optional): Birth year.
       - height (str, optional): Height.
       - mass (str, optional): Mass.
       - hair_color (str, optional): Hair color.
       - skin_color (str, optional): Skin color.
       - eye_color (str, optional): Eye color.
       - gender (str, optional): Gender.
       - homeworld (ID, optional): Relay global ID of home planet.
       - movies (list of ID, optional): List of movie Relay global IDs to associate.

    Returns:
       character (CharacterNode): The created character object.

    Raises:
        - Exception: If one or more Movie IDs are invalid.
        - Exception: If one Planet ID is invalid.
    """
    class Arguments:
        name = String(required=True)
        species = String()
        birth_year = String()
        movies = List(graphene.ID)

    character = Field(CharacterNode)

    def mutate(self, info, name, species=None, birth_year=None, height=None, mass=None, hair_color=None,
               skin_color=None, eye_color=None, gender=None, homeworld=None, movies=None):
        fields = dict(
            name=name,
            species=species or '',
            birth_year=birth_year or '',
            height=height or '',
            mass=mass or '',
            hair_color=hair_color or '',
            skin_color=skin_color or '',
            eye_color=eye_color or '',
            gender=gender or ''
        )

        # Add homeworld
        if homeworld:
            planet_instance = relay.Node.get_node_from_global_id(info, homeworld, only_type=PlanetNode)
            if planet_instance is None:
                raise Exception(f"Planet with id {homeworld} does not exist")
            fields["homeworld"] = planet_instance

        # Create Character
        character = Character(**fields)
        character.save()

        # Add Movies
        if movies:
            movie_instances = [
                relay.Node.get_node_from_global_id(info, movie_id, only_type=MovieNode)
                for movie_id in movies
            ]

            # Check if any of the IDs are invalid
            if None in movie_instances:
                raise Exception("One or more Movie IDs are invalid")

            character.movies.set(movie_instances)

        return CreateCharacter(character=character)


class Mutation(graphene.ObjectType):
    create_planet = CreatePlanet.Field()
    create_movie = CreateMovie.Field()
    create_character = CreateCharacter.Field()
