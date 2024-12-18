from graphene_federation import build_schema
from project_account.schema import Query as project_accounts_query
from project_account.views import Mutation as project_accounts_mutation
from project_uaa.schema import Query as project_uaa_query
from project_uaa.views import Mutation as project_uaa_mutation


class Query(project_accounts_query, project_uaa_query):
    pass

class Mutation(project_accounts_mutation,project_uaa_mutation):
    pass


schema = build_schema(query = Query, mutation=Mutation)