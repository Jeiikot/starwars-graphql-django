# Star Wars GraphQL API
![Build Status](https://github.com/Jeiikot/starwars-graphql-django/actions/workflows/ci-tests.yml/badge.svg)

A GraphQL API built with **Django** and **Graphene** to manage information from the Star Wars universe: characters, movies, and planets.
Easily query, create, and relate entities with full validation and real-world data.

---

📌 About This Repository & Branches

This project started as part of the LQN Technical Challenge.

   - The code submitted for the challenge is in the branch: lqn-technical-tes

   - The main and develop branches include further improvements.

   > Feel free to check the lqn-test branch for the exact version delivered for the technical assessment.
 
🌐 [Live Demo on Render](https://starwars-graphql-django.onrender.com/graphql/)

> Try the project live! Explore the API through the GraphiQL playground hosted on Render.

>  ⚠️ Note: It may take a few seconds to wake up if the server was inactive (free tier limitation).


---

## 🚀 Description

This project enables you to **query, filter, and create** characters, movies, and planets from the Star Wars universe through a **Relay-compatible GraphQL API**.

- List and search characters (with name filter)
- Query movies associated with each character
- Get detailed information about movies and planets
- Mutations to create characters, movies, and planets
- Easily relate entities and explore data
- Automated data loading from the public SWAPI
- Clean, modular, and validated codebase
- Dockerized environment for easy setup

---

## 📁 Project Structure & Technical Overview

```
starwars-graphql-django/
├── api/                      
├── services/                          
│ └── populate.py                      # Script to populate data from SWAPI.
├── starwars/                          # Django app.
│ ├── management/
│ │ └── commands/
│ │     └── load_starwars_data.py      # Custom management command to load data from SWAPI.
│ ├──  schema/                         
│     ├── mutations.py                 # GraphQL mutations.
│     ├── query.py                     # GraphQL queries.
│     └── types.py                     # GraphQL types.
│ └── tests/
│     ├──  test_characters.py          # Test GraphQL characters.
│     ├──  test_movies.py              # Test GraphQL movies.
│     ├──  test_mutations.py           # Test GraphQL mutations.
│     ├──  test_planets.py             # Test GraphQL planets.
│     └──  test_schema.py              # Test GraphQL schema.
│ └── models.py                        # Django models.
├── tests/
│ ├── conftest.py                      # Pytest configuration.
│ └── fixtures.py                      # Pytest fixtures.
├── utils/
│ ├── constants.py                      # Constants.
│ └── logger.py                         # Logger.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── manage.py
```

- **Django** + **Graphene** for a modern GraphQL API.
- **Custom management commands** for automated SWAPI data seeding.
- **Modular**: separation of API, business logic, and data models.
- **Testing**: with pytest and coverage.
- **Docker**: for easy local development.


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

5. **Load real Star Wars data automatically from SWAPI:**
   ```bash
     python manage.py load_starwars_data
   ```
   > **Tip:** This command fetches all characters, movies, and planets from the [public SWAPI](https://swapi.dev/), and loads them into your local database.

6. **(Optional) Run with Docker:**
   ```bash
    docker-compose up --build
   ```
   > Docker is fully supported for local development and testing.

7. **Start the development server (if not using Docker):**
   ```bash
    python manage.py runserver
   ```
---

## 🔎 Using the API (GraphQL Playground)

Open [`http://localhost:8000/graphql/`](http://localhost:8000/graphql/) in your browser to access the **GraphiQL** interface.  
You can explore the full API schema, run queries/mutations, and view in-code documentation.

---

### 🧩 Example Query: List Characters

```graphql
{
  allCharacters(name_Icontains: "luke") {
    edges {
      node {
        id
        name
        birthYear
        species
        homeworld { name }
        movies {
          edges {
            node {
              title
              openingCrawl
              director
              producers
              planets { edges { node { name } } }
            }
          }
        }
      }
    }
  }
}
```

---

### ✍️ Example Mutation: Create Character

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
      homeworld { name }
      movies { edges { node { title } } }
    }
  }
}
```

---

### 🌍 Example Mutation: Create Planet

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

### 🎬 Example Mutation: Create Movie

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
      planets { edges { node { name } } }
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

Then open `htmlcov/index.html` in your browser to see the coverage report.

---

## 📚 API Technical Documentation

- The API is fully self-documented via the **GraphiQL** explorer at [`/graphql/`](http://localhost:8000/graphql/).
- Each type, query, and mutation includes docstrings that appear as inline documentation in GraphiQL.
- All usage examples (queries, mutations) are available here and in GraphiQL.
- Automated data seeding from SWAPI simplifies onboarding and demos.

> **Note:** Swagger and Redoc are REST standards; for GraphQL, **interactive schema documentation** is the norm.

---

## 🐳 Docker Support

Build and start the project using Docker with:

```bash
  docker-compose up --build
```

All dependencies and environment setup are managed for you. Great for quick onboarding and teamwork.

---

---

## 🚀 Production Deployment (Gunicorn)

For production environments, use [Gunicorn](https://gunicorn.org/) as your WSGI server:

```bash
   gunicorn api.starwars.wsgi
```

---
## 📄 License

MIT

---

### 💡 **Highlights / What Makes This Project Professional**

- **Modern Django & GraphQL stack**
- **Automated real data loading** from public APIs
- **Clean, modular code structure**
- **Full Docker support**
- **Well-documented for easy onboarding**
- **Thorough testing & test coverage reporting**

---

> Automated testing and quality checks with [GitHub Actions](https://github.com/features/actions).