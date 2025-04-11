from typing import Dict

class Product:
    available_amount: int
    name: str
    price: float
    
    def __init__(self, name, price, available_amount):
        self.name = name
        self.price = price
        self.available_amount = available_amount
    
    def is_available(self, requested_amount):
        return self.available_amount >= requested_amount
    
    def buy(self, requested_amount):
        self.available_amount -= requested_amount
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __ne__(self, other):
        return self.name != other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name

class ShoppingCart:
    products: Dict[Product, int]
    
    def __init__(self):
        self.products = dict()
    
    def contains_product(self, product):
        return product in self.products
    
    def calculate_total(self):
        return sum([p.price * count for p, count in self.products.items()])
    
    def add_product(self, product: Product, amount: int):
        if not product.is_available(amount):
            raise ValueError(f"Product {product} has only {product.available_amount} items")
        self.products[product] = amount
    
    def remove_product(self, product):
        if product in self.products:
            del self.products[product]
    
    def submit_cart_order(self):
        for product, count in self.products.items():
            product.buy(count)
        self.products = dict()

class Order:
    cart: ShoppingCart
    
    def __init__(self, cart: ShoppingCart):
        self.cart = cart
    
    def place_order(self):
        self.cart.submit_cart_order() 