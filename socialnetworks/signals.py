from django.dispatch import Signal


# Signal sent when a user connects its account with a social profile.
connect = Signal(providing_args=['user', 'service'])

# Signal sent when a user disconnects its account from a social profile.
disconnect = Signal(providing_args=['user', 'service'])

# Signal sent when a user logs in with a social profile.
login = Signal(providing_args=['user', 'service'])
