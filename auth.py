from flask import g

from flask.ext.httpauth import HTTPBasicAuth

import models

basic_auth = HTTPBasicAuth()
auth = basic_auth


@basic_auth.verify_password
def verify_password(email_or_username, password):
    try:
        user = models.User.objects(
            Q(email=email) | Q(username__iexact=username)
        )
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True