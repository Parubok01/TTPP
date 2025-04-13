import unittest
from unittest.mock import patch, MagicMock
from eshop import Product, ShoppingCart, Order

class AdditionalProductTests(unittest.TestCase):
    def setUp(self):
        self.product = Product(name="Test Product", price=100.0, available_amount=10)
    
    def test_product_initialization(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.available_amount, 10)
    
    def test_product_availability_check(self):
        self.assertTrue(self.product.is_available(5))
        self.assertTrue(self.product.is_available(10))
        self.assertFalse(self.product.is_available(11))
    
    def test_product_buy_method(self):
        self.product.buy(3)
        self.assertEqual(self.product.available_amount, 7)
        self.product.buy(5)
        self.assertEqual(self.product.available_amount, 2)
    
    def test_product_buy_insufficient_amount(self):
        with self.assertRaises(ValueError):
            self.product.buy(11)
        self.assertEqual(self.product.available_amount, 10)  
    
    def test_product_equality(self):
        same_product = Product(name="Test Product", price=200.0, available_amount=5)
        different_product = Product(name="Different", price=100.0, available_amount=10)
        
        self.assertEqual(self.product, same_product)
        self.assertNotEqual(self.product, different_product)
        self.assertEqual(hash(self.product), hash(same_product))

class AdditionalShoppingCartTests(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.product1 = Product(name="Product1", price=50.0, available_amount=5)
        self.product2 = Product(name="Product2", price=75.0, available_amount=3)
    
    def test_empty_cart_total(self):
        self.assertEqual(self.cart.calculate_total(), 0)
    
    def test_cart_total_with_products(self):
        self.cart.add_product(self.product1, 2)
        self.cart.add_product(self.product2, 1)
        self.assertEqual(self.cart.calculate_total(), 175.0)  
    
    def test_remove_product_from_cart(self):
        self.cart.add_product(self.product1, 1)
        self.assertTrue(self.cart.contains_product(self.product1))
        self.cart.remove_product(self.product1)
        self.assertFalse(self.cart.contains_product(self.product1))
    
    def test_submit_cart_order(self):
        with patch.object(self.product1, 'buy') as mock_buy:
            self.cart.add_product(self.product1, 2)
            self.cart.submit_cart_order()
            mock_buy.assert_called_once_with(2)
            self.assertEqual(len(self.cart.products), 0)

class OrderTests(unittest.TestCase):
    def setUp(self):
        self.order = Order()
        self.order.cart = ShoppingCart()
        self.product = Product(name="Test", price=100.0, available_amount=5)
    
    def test_place_order(self):
        with patch.object(self.order.cart, 'submit_cart_order') as mock_submit:
            self.order.place_order()
            mock_submit.assert_called_once()

if __name__ == '__main__':
    unittest.main()