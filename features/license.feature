Feature: License-walling of unauthorized user

  Unauthorized user is user that didn't supply
  license yet. He should be redirected to license
  page when he tries to access any admin page on the site.
  User can access without valid license in prompt when valid license
  is already stored in DB.

  Scenario: Access of /admin/
    Given license wall is installed
    When user tries to access /admin/
    Then he should be redirected to /admin/login


  Scenario: Valid license is supplied
    Given user tries to access /admin/
    And user entered license
    When license is valid
    Then he should be redirected to /admin/

  Scenario: Invalid license is supplied
    Given user tries to access /admin/
    And user entered license
    When license is not valid
    Then he should be redirected to /admin/login
