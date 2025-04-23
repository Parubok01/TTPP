from eshop import Product, ShoppingCart, Order

def test_add_product():
    cart = ShoppingCart()
    p = Product("Book", 10, 11)
    cart.add_product(p, 7)
    assert cart.contains_product(p)
    assert len(cart.products) == 1
    assert cart.calculate_total() == (10 * 7) 

def test_product_creation():
    p = Product("Book", 10, 11)
    assert p.name == "Book"
    assert p.price == 10
    assert p.available_amount == 11

def test_product_availability():
    p = Product("Book", 10, 11)
    assert p.is_available(10) is True
    assert p.is_available(11) is True
    assert p.is_available(12) is False
    assert p.is_available(0) is False
    assert p.is_available(-1) is False

def test_buy_product():
    p = Product("Book", 10, 11)
    p.buy(5)
    assert p.available_amount == 6

def test_add_invalid_amount():
    cart = ShoppingCart()
    p = Product("Book", 10, 11)
    
    try:
        cart.add_product(p, 0)
        assert False, "Should raise ValueError for 0 amount"
    except ValueError:
        pass
    
    try:
        cart.add_product(p, -1)
        assert False, "Should raise ValueError for negative amount"
    except ValueError:
        pass

def test_add_unavailable_amount():
    cart = ShoppingCart()
    p = Product("Book", 10, 5)
    
    try:
        cart.add_product(p, 6)
        assert False, "Should raise ValueError for unavailable amount"
    except ValueError:
        pass

def test_remove_product():
    cart = ShoppingCart()
    p = Product("Book", 10, 11)
    cart.add_product(p, 7)
    assert cart.contains_product(p)
    
    cart.remove_product(p)
    assert not cart.contains_product(p)
    assert len(cart.products) == 0

def test_remove_nonexistent_product():
    cart = ShoppingCart()
    p = Product("Book", 10, 11)
    cart.remove_product(p) 

def test_calculate_total_empty_cart():
    cart = ShoppingCart()
    assert cart.calculate_total() == 0

def test_submit_cart_order():
    cart = ShoppingCart()
    p1 = Product("Book", 10, 11)
    p2 = Product("Pen", 5, 20)
    
    cart.add_product(p1, 2)
    cart.add_product(p2, 3)
    
    assert p1.available_amount == 11
    assert p2.available_amount == 20
    
    cart.submit_cart_order()
    
    assert p1.available_amount == 9
    assert p2.available_amount == 17
    assert len(cart.products) == 0

def test_place_order():
    cart = ShoppingCart()
    p = Product("Book", 10, 11)
    cart.add_product(p, 3)
    
    order = Order(cart)
    order.place_order()
    
    assert p.available_amount == 8
    assert len(cart.products) == 0 