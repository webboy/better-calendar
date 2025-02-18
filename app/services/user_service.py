from typing import List


class UserService:
    def is_validated(self, wa_id, phone_number) -> bool:
        """Placeholder for is_validated - to be implemented"""
        return True

    def get_user_by_wa_id(self, wa_id) -> str:
        """Placeholder for get_user_by_wa_id - to be implemented"""
        return "User"

    def get_user_list(self) -> List[str]:
        """Placeholder for get_user_list - to be implemented"""
        return ["User1", "User2"]

    def save_users(self, users: List[str]) -> None:
        """Placeholder for save_users - to be implemented"""
        pass