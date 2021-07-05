"""
Test cases for Product Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service import app
from service.models import Product, DataValidationError, db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
class TestProduct(unittest.TestCase):
    """ Test Cases for Product Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_find_by_name(self):
        """ Find products by Name """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_name("test2")
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")
  
    def test_find_by_price(self):
        """ Find products by Price """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_price(80, 90)
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")

    def test_find_by_owner(self):
        """ Find products by Owner """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_owner("test person2")
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")
