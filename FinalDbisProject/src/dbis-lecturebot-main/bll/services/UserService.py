from bll.dto.UserDTO import UserDTO
from bll.services.PasswordHashGeneratingService import PasswordHashGeneratingService

from dal.models.User import User
from dal.repositories.UserRepository import UserRepository


class UserService:
    def __init__(self, secret):
        self.user_repository = UserRepository()
        self.password_service = PasswordHashGeneratingService(secret)

    def register_user(self, user):
        user_to_register = User(
            login=user.Login,
            password=self.password_service.generate_password_hash(user.Password),
            role=user.Role,
            registration_date=user.RegistrationDate
        )

        if self.user_repository.get_user_by_key(user_to_register.Login):
            return "User with this name already exists!", 400
        else:
            self.user_repository.insert_user(user_to_register)
            return "User was successfully registered", 200

    def auth_user(self, user):
        user_to_auth = User(
            login=user.Login,
            password=self.password_service.generate_password_hash(user.Password),
            role=None,
            registration_date=None
        )

        user_to_compare = self.user_repository.get_user_by_key(user_to_auth.Login)

        if len(user_to_compare) == 0:
            return "Wrong username or password", 400
        elif user_to_compare[0].Password == user_to_auth.Password:
            return "Authentication is successful", 200
        else:
            return "Wrong username or password", 400
