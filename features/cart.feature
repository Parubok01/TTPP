Feature: Shopping cart
  We want to test that shopping cart functionality works correctly

  Scenario: Successful add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 123
    Then Product is added to the cart successfully

  Scenario: Failed add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 124
    Then Product is not added to cart successfully

  Scenario: Add product with zero amount
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount 0
    Then Product is not added to cart successfully

  Scenario: Add product with negative amount
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount -1
    Then Product is not added to cart successfully

  Scenario: Remove product from cart
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount 50
    And I remove the product from cart
    Then The cart should be empty

  Scenario: Calculate total price
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount 2
    Then The total price should be 246

  Scenario: Add multiple products to cart
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount 50
    And I add another product to the cart in amount 30
    Then The cart should contain 2 products

  Scenario: Submit order and clear cart
    Given The product has availability of 100
    And An empty shopping cart
    When I add product to the cart in amount 50
    And I submit the order
    Then The cart should be empty
    And The product availability should be 50

  Scenario: Try to add product with None amount
    Given The product has availability of 100
    And An empty shopping cart
    When I try to add product with invalid amount
    Then Product is not added to cart successfully

  Scenario: Try to add None product to cart
    Given An empty shopping cart
    When I try to add None product to cart
    Then Product is not added to cart successfully 