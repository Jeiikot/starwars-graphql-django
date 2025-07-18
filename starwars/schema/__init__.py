# Graphene
import graphene

# Schema
from starwars.schema.mutations import Mutation
from starwars.schema.query import Query


schema = graphene.Schema(query=Query, mutation=Mutation)
