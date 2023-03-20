from __future__ import annotations

import os

import pandas
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template import loader
from django.urls import reverse
from django_q.tasks import async_task

from app.models import MagicLink, Token


class Command(BaseCommand):
    help = "Creates users from a list of mail addresses"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, default=None)

    def handle(self, *args, **options):
        if not options["csv_file"]:
            raise CommandError("No list provided")
        file_path = options["csv_file"]
        cwd = os.getcwd()
        final_path = os.path.join(cwd, file_path)
        csv = pandas.read_csv(final_path)

        for _, row in csv.iterrows():
            try:
                User.objects.get(username=row["email"])
                self.stdout.write(
                    self.style.WARNING(f"User {row['email']} already exists")
                )
                continue
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=row["email"],
                    email=row["email"],
                )
                token = Token.create()
                magic_link = MagicLink.objects.create(user=user)

                template = loader.get_template("mail/magic_link.html")

                magic_link = f'{settings.DOMAIN}{reverse("app_login", kwargs={"token": magic_link.token})}'

                context = {
                    "name": user,
                    "magic_link": magic_link,
                    "passphrase": token,
                    "domain": settings.DOMAIN,
                    "subject": f"{settings.EMAIL_SUBJECT_PREFIX} Dein Abstimmungslink",
                }

                async_task(
                    send_mail,
                    subject=context["subject"],
                    message=f'Hallo {user},\nstimme ab mit folgendem Link:\n{context["magic_link"]}\n\nDein Prüfschlüssel lautet:\n{context["passphrase"]}\n\nBis dahin!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[f"{user.email}"],
                    html_message=template.render(context),
                    fail_silently=False,
                    q_options={"save": False},
                )

                self.stdout.write(f"User {row['email']} created")

        self.stdout.write(self.style.SUCCESS("Successfully created users"))
