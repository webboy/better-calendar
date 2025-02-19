# app/models/user.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    wa_id: Optional[str] = None
    reminder: Optional[int] = None
    validation_code: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_registered(self) -> bool:
        return bool(self.wa_id and self.phone_number)

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            wa_id=data.get('wa_id'),
            reminder=data.get('reminder'),  # Will be None if not present
            validation_code=data.get('validation_code')  # Will be None if not present
        )

    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'wa_id': self.wa_id,
            'reminder': self.reminder,
            'validation_code': self.validation_code
        }

    def update_whatsapp_info(self, phone_number: str, wa_id: str) -> None:
        self.phone_number = phone_number
        self.wa_id = wa_id