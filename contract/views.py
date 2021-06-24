import json
import re
from django.db.models import Q
from django.http import Http404
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, authentication, permissions
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Contract, SmartContract,ParticipationContract
from .serializers import ContractSerializer, SmartContractSerializer


class LatestContractsList(APIView):
    def get(self, request, format=None):

        contracts = Contract.objects.all()
        
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class ContractDetail(APIView):
    def get_object(self, smartcontract_slug, contract_slug):
        try:
            print("usersmartcontract")
            print(Contract.objects.filter(smartcontract__slug=smartcontract_slug).get(slug=contract_slug))
            return Contract.objects.filter(smartcontract__slug=smartcontract_slug).get(slug=contract_slug)
        except Contract.DoesNotExist:
            raise Http404
    
    def get(self, request, smartcontract_slug, contract_slug, format=None):
        contract = self.get_object(smartcontract_slug, contract_slug)
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

class SmartContractDetail(APIView):
    def get_object(self, smartcontract_slug):
        try:
            return SmartContract.objects.get(slug=smartcontract_slug)
        except SmartContract.DoesNotExist:
            raise Http404
    
    def get(self, request, smartcontract_slug, format=None):
        smartcontract = self.get_object(smartcontract_slug)
        serializer = SmartContractSerializer(smartcontract)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    print("works!!!!!!!!!!!!!!!!!!!!!")
    if query:
        contracts = Contract.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)
    else:
        return Response({"contract": []})

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class UserContractsList(APIView):
    def get(self, request, format=None):
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        contracts = Contract.objects.filter(id_create=request.user)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class UserParticipationList(APIView):
    def get(self, request, format=None):
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        contracts = Contract.objects.filter(contract_id_participation__user_id=request.user)
        print(contracts)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)        




@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def contractAdd(request):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print(request.body)
    data=json.loads(request.body)
    print(request.user)
    newContract=Contract(smartcontract=SmartContract.objects.get(pk=data['SmartContract']),name=data['name'],address=data['address'],slug=data['slug'],description=data['description'],price=data['price'],image=data['image'],thumbnail=data['thumbnail'],
                            id_create=request.user
                        )
    newContract.save()
    return Response( status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def participation(request):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    data=json.loads(request.body)
    participation_id=ParticipationContract(user=request.user,contract_id=Contract.objects.get(address=data["address"]))
    participation_id.save()
    return Response     

