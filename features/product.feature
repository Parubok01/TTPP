Feature: Product
  We want to test that product functionality works correctly

  Scenario: Check product availability
    Given A product with availability of 100
    When I check availability for amount 50
    Then The product should be available

  Scenario: Check product unavailability
    Given A product with availability of 100
    When I check availability for amount 150
    Then The product should not be available

  Scenario: Buy product and check availability
    Given A product with availability of 100
    When I buy 30 units
    Then The product availability should be 70

  Scenario: Try to buy more than available
    Given A product with availability of 100
    When I try to buy 150 units
    Then The operation should fail

  Scenario: Buy zero units
    Given A product with availability of 100
    When I try to buy 0 units
    Then The operation should fail

  Scenario: Buy negative units
    Given A product with availability of 100
    When I try to buy -10 units
    Then The operation should fail

  Scenario: Compare equal products
    Given Two products with same name
    When I compare them
    Then They should be equal

  Scenario: Compare different products
    Given Two products with different names
    When I compare them
    Then They should not be equal

  Scenario: Create product with zero price
    Given I try to create a product with zero price
    When The product is created
    Then The price should be 0

  Scenario: Create product with negative price
    Given I try to create a product with negative price
    When The product is created
    Then The price should be negative 