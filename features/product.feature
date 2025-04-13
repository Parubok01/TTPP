Feature: Product availability
  Test product availability logic

  Scenario: Product is available
    Given A product "Phone" with price 1000 and availability 5
    When I check availability for 3
    Then The product is available

  Scenario: Product is not available
    Given A product "Phone" with price 1000 and availability 5
    When I check availability for 10
    Then The product is not available

  Scenario: Product availability is zero
    Given A product "Tablet" with price 500 and availability 0
    When I check availability for 1
    Then The product is not available

  Scenario: Product availability is equal to requested
    Given A product "Camera" with price 750 and availability 5
    When I check availability for 5
    Then The product is available

  Scenario: Product with negative availability
    Given A product "TV" with price 300 and availability -1
    When I check availability for 1
    Then The product is not available

  Scenario: Product with zero requested
    Given A product "Mouse" with price 25 and availability 10
    When I check availability for 0
    Then The product is available

  Scenario: Product with negative requested
    Given A product "Keyboard" with price 45 and availability 5
    When I check availability for -3
    Then The product is available

  Scenario: Product is None
    Given No product is defined
    When I check availability for 1
    Then The product check fails

  Scenario: Product with None as availability
    Given A product with None availability
    When I check availability for 1
    Then The product check fails

  Scenario: Product with non-numeric availability
    Given A product with string availability "many"
    When I check availability for 1
    Then The product check fails
