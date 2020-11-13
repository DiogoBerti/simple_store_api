import pytest
from . import models
from rest_framework.test import APIRequestFactory
import os
import re

# SETUP
@pytest.fixture
def api_client():   
   return APIRequestFactory()


@pytest.fixture
def object_client():
    return models.Client.objects.create(**{
        "name":"Cliente Teste",
        "doc":"12345647891",
        "phone":"11955771179",
        "address":"Avenida Paulista 123",
        "type_person":"1",
    })

@pytest.fixture
def object_product():
    return models.Product.objects.create(**{
        "name":"Caixa de Leite",
        "price":15,
        "weight":10,
        "type_product":"1",        
    })

@pytest.fixture
def object_product_second():
    return models.Product.objects.create(**{
        "name":"Chocolate em barra",
        "price":3.5,
        "weight":1,
        "type_product":"1",        
    })

@pytest.fixture
def object_sale_order(object_client):
    return models.SaleOrder.objects.create(**{
        "client": object_client,
        "date_order":"2020-11-01",
        "total_value":0,        
    })

@pytest.fixture
def object_sale_line(object_sale_order, object_product):
    return models.SaleOrderLine.objects.bulk_create([
        models.SaleOrderLine(**{
            "order": object_sale_order,
            "product":object_product,
            "quantity":1,        
            "discount":0,        
        }),
        models.SaleOrderLine(**{
            "order": object_sale_order,
            "product":object_product,
            "quantity":3,        
            "discount":10,        
        }),    
    ])

# Testing Objects..
@pytest.mark.django_db
class TestClientProductCompany:
    """
        Testing Clients...
    """

    def test_client_create(self, object_client):
        # Testing client creation
        assert object_client, "Client not created"

    def test_client_update(self, object_client):
        # Testing client update
        object_client.name = "Other Name"
        assert object_client, "Client not created"
        assert (object_client.name == "Other Name"), "Client was not renamed"

@pytest.mark.django_db
class TestSaleOrder:
    """
        Testing Sale Orders...
    """
    def test_order_create(self, object_sale_order, object_sale_line):
        # Testing Order creation
        assert object_sale_order, "Order not created"
        assert object_sale_line, "Order Line not created"
        assert object_sale_order.total_value_order == 50, "Wrong calculation of total value"

    def test_order_defaults(self, object_sale_order, object_sale_line):
        # Testing Order Defaults         
        assert object_sale_order.type_of_payment == "1", "Default Payment Type not setted"
        assert isinstance(object_sale_order.lines, list), "Could not get an Array of lines"  

    def test_order_by_client(self, object_sale_order, object_sale_line, object_client):
        # Testing Order by clients          
        assert len(object_client.get_sales) == 1, "Some sale order was not setted for this client..."
        assert object_client.get_sales_spent == 50, "Orders assigned to client are wrong"  
    
    def test_order_update(self, object_sale_order, object_sale_line, object_client, object_product_second):
        # Testing Order Changes...                 
        assert object_client.get_sales_spent == 50, "Orders Totals were not calculated right firstly"  
        object_sale_line[1].product = object_product_second
        object_sale_line[1].save()
        assert object_client.get_sales_spent == 15.5, "Orders Totals were not calculated right after change"  

@pytest.mark.django_db
class TestAPIs:
    """
        Testing Apis...
    """
    def test_client_api(self, api_client):
        posted = api_client.post("/api/v1/clients", {'name': 'Testing User'})        
        assert posted, "Post data did not work"
        assert posted.status_code in [200,201], "Post data Rejected"
        