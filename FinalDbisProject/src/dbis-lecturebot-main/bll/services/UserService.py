from bll.dto.UserDTO import UserDTO
from bll.services.PasswordHashGeneratingService import PasswordHashGeneratingService

from dal.models.User import User
from dal.repositories.UserRepository import UserRepository


# noinspection PyBroadException
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

    def promote_user(self, user_login, new_role):
        user_to_promote = self.user_repository.get_user_by_key(user_login)[0]
        user_to_promote.Role = new_role

        try:
            self.user_repository.update_user_fields(user_to_promote)
            return "User was successfully promoted!", 200
        except Exception:
            return "Oops, something went wrong!", 500

    def get_user_by_login(self, login):
        user = self.user_repository.get_user_by_key(login)[0]
        return UserDTO(
            login=user.Login,
            password=user.Password,
            registration_date=user.RegistrationDate,
            role=user.Role
        )

    def get_all_users(self):
        users = self.user_repository.get_all_users()
        mapped_users = [UserDTO(
            login=user.Header,
            role=user.Role,
            password=user.Password,
            registration_date=user.RegistrationDate
        ) for user in users]

        return mapped_users
