import pytest
from src.dra818vhf import DRA818VHF

volumes = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

@pytest.fixture(scope='module')
def instance():
    myobj = DRA818VHF()
    return(myobj)

@pytest.mark.parametrize('vols', volumes)
def test_volume_vals(vols, instance):
    assert instance.check_volume(setvol=vols)