import pytest
import glob
from captcha import Captcha
import os


@pytest.fixture(params=glob.glob("test/fixtures/captcha/*.png"))
def captcha_image(request):
    yield request.param


def test_captcha(captcha_image):
    filename = os.path.basename(captcha_image)
    assert Captcha().decaptcha(captcha_image) == filename[:-4]
