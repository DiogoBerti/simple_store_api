import pytest
from . import models
from rest_framework.test import APIClient
from django.test import RequestFactory
from django.contrib.auth.models import User
import os
import re

# SETUP
@pytest.fixture
def api_client():   
   return APIClient()


@pytest.fixture
def object_user():
    return User.objects.create(**{
        "password": "pbkdf2_sha256$150000$QSJcNYRxX3oO$nfLSNlx87nyv+XpQLH/soBu8j5FipwWHJuanmjkO7EI=",
        "last_login": None,
        "is_superuser": True,
        "username": "root",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": True,
        "is_active": True,
        "date_joined": "2020-11-11T20:15:30.547Z",   
    })

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
class TestClientProduct:
    """
        Testing Clients And products...
    """

    def test_client_create(self, object_client):
        print("\n______STARTING ALL TESTS__________")
        # Testing client creation
        assert object_client, "Client not created"

    def test_client_update(self, object_client):
        print("______TESTING CLIENT CREATION__________")
        # Testing client update
        object_client.name = "Other Name"        
        assert (object_client.name == "Other Name"), "Client was not renamed"
    
    def test_product_create(self, object_product):        
        print("______TESTING PRODUCTS__________")
        # Testing Product creation
        assert object_product, "Product not created"

    def test_product_update(self, object_product):
        # Testing product update
        object_product.name = "Caixa de Bom bom"        
        assert (object_product.name == "Caixa de Bom bom"), "Product was not renamed"

@pytest.mark.django_db
class TestSaleOrder:
    """
        Testing Sale Orders...
    """
    def test_order_create(self, object_sale_order, object_sale_line):
        print("______TESTING SALE ORDERS__________")
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
    def test_client_api(self, api_client, object_user):
        '''
            Setting API the API user and doing some requests...
        '''
        print("______TESTING APIS__________")
        # Login URL
        create_login = api_client.post("/api/token/", {
            "username":"root",
            "password":"admin"
        })        
        assert "access" in create_login.data.keys(), "Could not Authenticate User"
        
        # Trying to Get Without Autth
        gettting = api_client.get("/api/v1/clients/")
        assert gettting.status_code not in [200,201], "Get data Should not Work"
        # Loggin In User
        api_client.login(username='root', password='admin')
        # Tryiing to Get Authenticated
        gettting_logged = api_client.get("/api/v1/clients/")
        assert gettting_logged.status_code in [200,201], "Get was Rejected"
        
    def test_product_api(self, api_client, object_user):
        '''
            Testing the products API
        '''                      
        # Trying to Get Without Auth
        gettting = api_client.get("/api/v1/products/")
        assert gettting.status_code not in [200,201], "Get data Should not Work"
        # Loggin In User
        api_client.login(username='root', password='admin')
        # GET
        gettting_logged = api_client.get("/api/v1/products/")
        assert gettting_logged.status_code in [200,201], "Get on Products was Rejected"
        # POST
        posting_product = api_client.post("/api/v1/products/", {
            "name":"Testing Product",
            "price":10,
            "weight":1,
            "type_product":"1",   
        })
        assert posting_product.status_code in [200,201], "Post on Products was Rejected"
        assert models.Product.objects.all().count() == 1, "Product was not Created.."
        # PATCH
        prod_id = models.Product.objects.first()
        api_client.patch("/api/v1/products/{}/".format(prod_id.id), {
            "name":"New Product",
        })
        assert models.Product.objects.all().count() == 1, "Product was Deleted Wrongly.."
        assert models.Product.objects.first().name == "New Product", "Product Patch did not work."
        # DELETE
        api_client.delete("/api/v1/products/{}/".format(prod_id.id))
        assert models.Product.objects.all().count() < 1, "Product was not Deleted.."
        
    def test_saleorder_api(self, api_client, object_user, object_client, object_product):
        '''
            Testing the Sales API
        '''                      
        # Trying to Get Without Auth
        gettting = api_client.get("/api/v1/order/")
        assert gettting.status_code not in [200,201], "Get data Should not Work"
        # Loggin In User
        api_client.login(username='root', password='admin')
        # GET
        gettting_logged = api_client.get("/api/v1/order/")
        assert gettting_logged.status_code in [200,201], "Get on order was Rejected"
        # POST
        order_data =  {
            "client": object_client.id,
            "type_of_payment": "1",                   
        }        
        posting_order = api_client.post("/api/v1/order/",order_data)        
        assert posting_order.status_code in [200,201], "Post on order was Rejected"
        assert models.SaleOrder.objects.all().count() == 1, "Sale Order was not Created.."
        del order_data
        # PATCH
        order_id = models.SaleOrder.objects.first()
        api_client.patch("/api/v1/order/{}/".format(order_id.id), {
            "type_of_payment": "2",  
        })
        assert models.SaleOrder.objects.all().count() == 1, "Order was Deleted Wrongly.."
        assert models.SaleOrder.objects.first().type_of_payment == "2", "Order Patch did not work."
        
        # ORDER LINE Testing...
        posting_order_line = api_client.post("/api/v1/order_lines/",{
            "order":order_id.id,
            "product": object_product.id,
            "quantity": 1
        })        
        assert posting_order_line.status_code in [200,201], "Post on order Line was Rejected"
        assert models.SaleOrderLine.objects.all().count() == 1, "Order Line was not Created.."    
        del order_id
        # Checking order line inside order
        order_id = models.SaleOrder.objects.first()
        assert order_id.lines, "Lines were not uploaded to Order"
        assert len(order_id.lines) == 1, "Lines Were not added correctly to order"
        # DELETE
        api_client.delete("/api/v1/order/{}/".format(order_id.id))
        assert models.SaleOrder.objects.all().count() < 1, "Product was not Deleted.."

        