import pytest
from app.services.user_service import UserService, User

@pytest.fixture()
def user_service():
    return UserService('package.json')


def test_get_user_by_email_invalid(user_service):
    with pytest.raises(ValueError):
        user_service.get_user_by_email('potato')


def test_get_user_by_email_valid(user_service):
    user = user_service.get_user_by_email('extramedia.nemanja@gmail.com')
    assert isinstance(user, User), "Expected User instance but got something else."

def test_get_user_by_wa_id_valid(user_service):
    user = user_service.get_user_by_wa_id('491724184069')
    assert isinstance(user, User), "Expected User instance but got something else."


def test_get_user_by_wa_id_invalid(user_service):
    assert user_service.get_user_by_wa_id('00') is None, "Expected None for non-existent user."

if __name__ == '__main__':
    pytest.main()
