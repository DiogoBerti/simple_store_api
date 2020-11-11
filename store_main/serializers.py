from rest_framework import serializers
from . import models

class ClientSerializer(serializers.ModelSerializer):
    """
        Serializer for Clients
    """    
    class Meta:
        model = models.Client
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    """
        Serializer for Product
    """
    class Meta:
        model = models.Product
        fields = "__all__"

class SaleOrderLineSerializer(serializers.ModelSerializer):
    """
        Serializer for SaleOrderLine
    """
    
    class Meta:
        model = models.SaleOrderLine
        fields = "__all__"


class SaleOrderSerializer(serializers.ModelSerializer):
    """
        Serializer for SaleOrder
    """
    lines = SaleOrderLineSerializer(many=True, write_only=True)
    lines_from_order = serializers.SerializerMethodField('get_lines', read_only=True)    
    total_value = serializers.SerializerMethodField('get_total_value', read_only=True)    

    def get_lines(self, obj):
        return obj.lines

    def get_total_value(self, obj):
        return obj.total_value_order

    def create(self, validated_data):
        '''
            Receiving the data from lines and Orders and generate the respective
            registers.
        '''
        lines_to_update = validated_data.pop('lines')        
        instance = models.SaleOrder.objects.create(**validated_data)
        for line in lines_to_update:            
            models.SaleOrderLine.objects.create(order=instance, **line)        
        return instance

    class Meta:
        model = models.SaleOrder
        fields = "__all__"



