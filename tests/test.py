import pytest

from chromeintern import get_local_release

def test_get_local_release():
    release = get_local_release()
    assert isinstance(release, str)
