from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from reviews.models import User


def send_mail_confirmation_code(username: str) -> None:
    user = get_object_or_404(User, username=username)
    user.email_user(
        subject="Код подтверждения регистрации",
                message="confirmation_code: "
                        f"{default_token_generator.make_token(user)}",
                from_email='a@a.ru',
    )
