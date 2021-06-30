from rest_framework import serializers

from .models import SmartContract, Contract

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
            "address",
            "smartcontract_id"
        )

class SmartContractSerializer(serializers.ModelSerializer):
    contracts = ContractSerializer(many=True)

    class Meta:
        model = SmartContract
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "contracts",
        )