import pytest
import glob
from courts import Courts
import os

def test_courts_generator():
    courts = list(Courts())
    assert len(courts) == 39

    assert courts[0].state_cd == "1"
    assert courts[0].dist_cd == "1"
    assert courts[0].court_code == None
        
