import pytest

from chromeguard import ChromeDriver


def test_chromedriver_init():
    driver = ChromeDriver()
    assert isinstance(driver, ChromeDriver)


def test_parse_chromedriver_version():
    driver = ChromeDriver()
    VERSION = ('ChromeDriver 2.37.544315 (730aa6a5fdba159ac9f4c1e8cbc59bf1b5ce'
               '12b7)')
    parsed_version = driver.parse_chromedriver_version(VERSION)
    EXPECTED_VERSION = '2.37'
    assert parsed_version == EXPECTED_VERSION
