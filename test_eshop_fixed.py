import unittest
from eshop import Product, ShoppingCart, Order

from test_eshop import *

class TestMutationKiller(unittest.TestCase):
    def test_kill_surviving_mutations(self):
        product = Product("Test", 10, 5)
        
        assert product.is_available(5) is True, "Exact match should be available"
        
        assert product.is_available(4) is True, "Less than available should be available"
        
        assert product.is_available(6) is False, "More than available should not be available"
    
    def test_kill_lte_eq_mutation(self):
        p = Product("MutationKiller1", 10, 5)
        
        self.assertTrue(p.is_available(5), "Exact amount should be available")
        
        self.assertTrue(p.is_available(4), "Less than available amount should be available")
        self.assertTrue(p.is_available(1), "Much less than available amount should be available")
        
        self.assertFalse(p.is_available(6), "More than available should not be available")
        self.assertFalse(p.is_available(100), "Much more than available should not be available")
    
    def test_kill_lte_lt_mutation(self):
        p = Product("MutationKiller2", 10, 5)
        
        self.assertTrue(p.is_available(5), "Exact amount should be available")
        
        self.assertTrue(p.is_available(4), "Less than available should be available")
        self.assertFalse(p.is_available(6), "More than available should not be available")
    
    def test_add_product_exact_amount(self):
        cart = ShoppingCart()
        p = Product("ExactAmount", 10, 5)
        
        cart.add_product(p, 5)
        self.assertEqual(cart.products[p], 5, "Should allow adding exactly available amount")
        
        cart = ShoppingCart()
        p2 = Product("AnotherItem", 15, 7)
        
        with self.assertRaises(ValueError):
            cart.add_product(p2, 8) 
        
        cart.add_product(p2, 7)  
        self.assertEqual(cart.products[p2], 7)
    
    def test_exhaustive_boundary_testing(self):
        p = Product("ComprehensiveTest", 10, 5)
        
        for amount in [-100, -10, -1, -0.1, 0]:
            self.assertFalse(p.is_available(amount), 
                            f"Amount {amount} should not be available")
        
        for amount in [0.1, 1, 4, 4.9, 5]:
            self.assertTrue(p.is_available(amount),
                           f"Amount {amount} should be available")
        
        for amount in [5.1, 6, 10, 100]:
            self.assertFalse(p.is_available(amount),
                            f"Amount {amount} should not be available")
    
    def test_cart_add_product_exact_quantity(self):
        cart = ShoppingCart()
        
        products = [
            Product("Item1", 10, 3),
            Product("Item2", 15, 5),
            Product("Item3", 20, 7)
        ]
        
        for p in products:
            exact_amount = p.available_amount
            cart.add_product(p, exact_amount)
            self.assertEqual(cart.products[p], exact_amount,
                            f"Should be able to add exactly {exact_amount} of {p.name}")
        
        expected_total = sum(p.price * p.available_amount for p in products)
        self.assertEqual(cart.calculate_total(), expected_total)

if __name__ == "__main__":
    unittest.main()