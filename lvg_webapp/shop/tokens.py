from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailChangeTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Hash includes user ID, timestamp, and current email
        return f"{user.pk}{timestamp}{user.email}"

email_change_token = EmailChangeTokenGenerator()
