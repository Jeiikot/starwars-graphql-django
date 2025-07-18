# Models
from starwars.models import Planet, Movie, Character

# Externals
import requests

# Utils
from utils.logger import logger


STAR_WARS_API = "https://swapi.dev/api/"


def fetch_all(url):
    """
    Fetch all data from a SWAPI endpoint.

    Args:
        url (str): The URL to fetch data from.
    Returns:
        list: A list of dictionaries containing the fetched data.
    """
    results = []
    while url:
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            results.extend(data["results"])
            url = data.get("next")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            break
    return results

def get_swapi_id_from_url(url):
    return int(url.rstrip('/').split('/')[-1])

def populate_planets():
    """
    Populate the Planet model with data from the SWAPI.
    """
    logger.info("Populating planets...")

    # Initialize variables
    existing_ids = set(Planet.objects.values_list('swapi_id', flat=True))
    new_planets = list()

    for planet in fetch_all(f"{STAR_WARS_API}planets/"):
        # Skip existing planet
        swapi_id = get_swapi_id_from_url(planet["url"])
        if swapi_id in existing_ids:
            continue

        new_planets.append(
            Planet(
                swapi_id=swapi_id,
                name=planet["name"],
                climate=planet.get("climate", ""),
                terrain=planet.get("terrain", ""),
                rotation_period=planet.get("rotation_period", ""),
                orbital_period=planet.get("orbital_period", ""),
                diameter=planet.get("diameter", ""),
                gravity=planet.get("gravity", ""),
                surface_water=planet.get("surface_water", ""),
                population=planet.get("population", ""),
            )
        )

    # Bulk create the new planets
    created_planets = Planet.objects.bulk_create(new_planets)
    logger.info(f"{len(created_planets)} planets created.")
    return created_planets

def populate_movies():
    """
    Populate the Movie model with data from the SWAPI.
    """
    logger.info("Populating movies...")

    # Initialize variables
    existing_ids = set(Movie.objects.values_list('swapi_id', flat=True))
    films = fetch_all(f"{STAR_WARS_API}films/")
    planets_map = {p.swapi_id: p for p in Planet.objects.all()}
    new_movies = []
    films_map = {}

    for film in films:
        # Skip existing film
        swapi_id = get_swapi_id_from_url(film["url"])
        films_map[swapi_id] = film

        if swapi_id in existing_ids:
            continue

        new_movies.append(
            Movie(
                swapi_id=swapi_id,
                title=film["title"],
                episode_id=film["episode_id"],
                opening_crawl=film["opening_crawl"],
                director=film["director"],
                producers=film["producer"],
                release_date=film["release_date"],
            )
        )

    created_movies = Movie.objects.bulk_create(new_movies)
    logger.info(f"{len(created_movies)} movies created.")

    # Add planets
    for movie in created_movies:
        film = films_map.get(movie.swapi_id)
        if not film:
            continue

        for planet_url in film.get("planets", []):
            planet_id = get_swapi_id_from_url(planet_url)
            planet = planets_map.get(planet_id)
            if planet:
                movie.planets.add(planet)

    logger.info("Movies populated with planets.")
    return created_movies

def populate_characters():
    """
    Populate the Character model with data from the SWAPI.
    """
    logger.info("Populating characters...")

    # Initialize variables
    existing_ids = set(Character.objects.values_list('swapi_id', flat=True))
    characters_data = fetch_all(f"{STAR_WARS_API}people/")
    planets_map = {p.swapi_id: p for p in Planet.objects.all()}
    movies_map = {m.swapi_id: m for m in Movie.objects.all()}
    new_characters = []
    characters_map = {}

    for character in characters_data:
        # Skip existing character
        swapi_id = get_swapi_id_from_url(character["url"])
        characters_map[swapi_id] = character

        if swapi_id in existing_ids:
            continue

        # Get homeworld
        homeworld_id = get_swapi_id_from_url(character["homeworld"]) if character.get("homeworld") else None
        homeworld = planets_map.get(homeworld_id) if homeworld_id else None

        new_characters.append(
            Character(
                swapi_id=swapi_id,
                name=character.get("name", ""),
                birth_year=character.get("birth_year", ""),
                species=", ".join(character.get("species", [])),
                height=character.get("height", ""),
                mass=character.get("mass", ""),
                hair_color=character.get("hair_color", ""),
                skin_color=character.get("skin_color", ""),
                eye_color=character.get("eye_color", ""),
                gender=character.get("gender", ""),
                homeworld=homeworld,
            )
        )

    created_characters = Character.objects.bulk_create(new_characters)
    logger.info(f"{len(created_characters)} characters created.")

    # Add movies
    for charecter in created_characters:
        character_data = characters_map.get(charecter.swapi_id)
        if not character_data:
            continue

        for film_url in character_data.get("films", []):
            film_id = get_swapi_id_from_url(film_url)
            movie = movies_map.get(film_id)
            if movie:
                charecter.movies.add(movie)

    logger.info("Characters populated with movies.")
    return created_characters
