import graphene
from .models import *
from graphene_django.types import DjangoObjectType

class Amount(graphene.ObjectType):
    unit = graphene.String()
    value = graphene.Float()




class AccountBalance(graphene.ObjectType):
    balanceType = graphene.String()
    amount = graphene.Field(Amount)
class Query(graphene.ObjectType):
    bill_list = graphene.String(dataModel=graphene.String(required=False), 
                                accountNo=graphene.Int(required=False), 
                                state=graphene.String(required=False))

    def resolve_bill_list(self, info, **kwargs):
        # Assuming you have a function to fetch the bill list
        # For example, fetching from a database or an API
        # Here we just return a dummy string for demonstration
        dataModel = kwargs.get('dataModel', 'Internal')
        accountNo = kwargs.get('accountNo', None)
        state = kwargs.get('state', None)
        print(self.request)
        


        return f"Bill list for {dataModel} with age {accountNo}"
schema = graphene.Schema(query=Query)