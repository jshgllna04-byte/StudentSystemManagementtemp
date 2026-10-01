from features.auth.model import MIN_PASSWORD_LENGTH
from features.auth.repository import insert_user, select_user


def register(user_name, password, confirm_password):
    if not user_name or not password or not confirm_password:
        return False, "Missing Information", "Please fill in all fields."

    if password != confirm_password:
        return False, "Password Error", "Passwords do not match."

    if len(password) < MIN_PASSWORD_LENGTH:
        return (
            False,
            "Password Error",
            "Password must contain at least 4 characters.",
        )

    if not insert_user(user_name, password):
        return (
            False,
            "Username Exists",
            "That username is already registered.",
        )

    return True, "Success", "Account created successfully."


def login(user_name, password):
    if not user_name or not password:
        return (
            None,
            "Invalid information",
            "please enter username and password",
        )

    user = select_user(user_name, password)

    if not user:
        return None, "Login Failed", "Invalid Username or Password"

    return user, "", ""
