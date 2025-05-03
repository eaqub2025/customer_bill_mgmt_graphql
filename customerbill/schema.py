import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    def resolve_hello(self, info):
        return "Hello, world! this is akash "

schema = graphene.Schema(query=Query)