import sys
import os
import pytest

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.validation_service import ValidationService

@pytest.fixture
def validation_service():
    return ValidationService()


def test_validate_email():
    assert ValidationService.validate_email("test@example.com") is True
    assert ValidationService.validate_email("user.name+potato@gmail.com") is True
    assert ValidationService.validate_email("coooooolllbro") is False
    assert ValidationService.validate_email("@potato.com") is False
    assert ValidationService.validate_email("user@.com") is False
    assert ValidationService.validate_email("user@com") is False
    assert ValidationService.validate_email("nemanjia@hotmail..com") is True
def test_validate_reminder_time(validation_service):
    assert validation_service.validate_reminder_time("5") is True
    assert validation_service.validate_reminder_time("10") is True
    assert validation_service.validate_reminder_time("15") is True

    assert validation_service.validate_reminder_time("0") is False
    assert validation_service.validate_reminder_time("20") is False
    assert validation_service.validate_reminder_time("abc") is False
    assert validation_service.validate_reminder_time("-5") is False


if __name__ == "__main__":
    pytest.main()
