# coding: utf-8

import unittest
import pytest
import captcha
import glob

@pytest.fixture()
def captcha_image():
	for f in glob.glob("test/fixtures/*.png"):
		yield f

def test_captcha(captcha_image):
	assert captcha.decaptcha(captcha_image) == "abcde"