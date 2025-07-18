
# Star Wars GraphQL API

A GraphQL API built with **Django** and **Graphene** to manage information from the Star Wars universe: characters, movies, and planets.

---

## 🚀 Description

This project allows you to query, filter, and create characters, movies, and planets from the Star Wars universe through a Relay-compatible GraphQL API.

- List and search characters (name filter)
- Query movies associated with each character
- Detailed information about movies and planets
- Mutations to create characters, movies, and planets
- Easily relate characters, movies, and planets
- Clean, validated, and documented code

---

## 🛠️ Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your_user/starwars-graphql-django.git
   cd starwars-graphql-django
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the database and run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load initial data from SWAPI:**
   ```bash
   python manage.py load_starwars_data
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

---

## 🔎 Using the API (GraphQL Playground)

Go to `http://localhost:8000/graphql/` to explore the API using GraphiQL or any GraphQL client.

---

### **Example Query: List Characters**

```graphql
{
  allCharacters(name_Icontains: "luke") {
    edges {
      node {
        id
        name
        birthYear
        species
        homeworld {
          name
        }
        movies {
          edges {
            node {
              title
              openingCrawl
              director
              producers
              planets {
                edges {
                  node {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

### **Example Mutation: Create Character**

```graphql
mutation {
  createCharacter(
    name: "Ahsoka Tano",
    species: "Togruta",
    birthYear: "36BBY",
    homeworld: "<PLANET_ID>",
    movies: ["<MOVIE_ID_1>", "<MOVIE_ID_2>"]
  ) {
    character {
      id
      name
      homeworld {
        name
      }
      movies {
        edges {
          node {
            title
          }
        }
      }
    }
  }
}
```

---

### **Example Mutation: Create Planet**

```graphql
mutation {
  createPlanet(
    name: "Kamino",
    climate: "temperate",
    terrain: "ocean",
    population: "1000000"
  ) {
    planet {
      id
      name
      climate
    }
  }
}
```

---

### **Example Mutation: Create Movie**

```graphql
mutation {
  createMovie(
    title: "The Mandalorian",
    episodeId: 10,
    openingCrawl: "A new story in the galaxy...",
    director: "Jon Favreau",
    producers: "Dave Filoni, Jon Favreau",
    releaseDate: "2023-12-12",
    planets: ["<PLANET_ID_1>"]
  ) {
    movie {
      id
      title
      director
      planets {
        edges {
          node {
            name
          }
        }
      }
    }
  }
}
```

---

## 🧪 Testing

Run the tests with:

```bash
  pytest
```
---

## 🛡️ Test Coverage

To run the tests with coverage, use:

```bash
  pytest --cov=starwars
```

To generate a coverage HTML report:

```bash
  pytest --cov=starwars --cov-report=html
```

Then open htmlcov/index.html in your browser to see the coverage report.

---

## 📚 API Technical Documentation

This API is fully self-documented using the GraphiQL interface available at [`/graphql/`](http://localhost:8000/graphql/).

- **GraphiQL** is an interactive in-browser tool that allows you to explore all queries, mutations, types, and see their descriptions (taken from the code docstrings).
- All mutations, queries, and fields include inline documentation.
- Example queries and mutations are available directly in the README and in the GraphiQL documentation explorer.

**Note:** Swagger and Redoc are standards for REST APIs, but are not commonly used in GraphQL projects.  
In GraphQL, the best practice is interactive schema documentation with GraphiQL.

---