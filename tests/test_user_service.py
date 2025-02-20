import sys
import os
import pytest

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.user_service import UserService, User

@pytest.fixture()
def user_service():
    return UserService('tests\\package.json')


def test_get_user_by_email_invalid(user_service):
    with pytest.raises(ValueError):
        user_service.get_user_by_email('potato')


def test_get_user_by_email_valid(user_service):
    user = user_service.get_user_by_email('extramedia.nemanja@gmail.com')
    assert isinstance(user, User), "Fail"

def test_get_user_by_wa_id_valid(user_service):
    user = user_service.get_user_by_wa_id('491724184069')
    assert isinstance(user, User), "Fail"


def test_get_user_by_wa_id_invalid(user_service):
    assert user_service.get_user_by_wa_id('00') is None, "Fail"
    assert user_service.get_user_by_wa_id(12) is None, "Fail"

if __name__ == '__main__':
    pytest.main()
