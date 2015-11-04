# -*- coding: utf-8 -*-
def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        SECRET_KEY='ThisIsNotSecret',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'socialnetworks',
            'socialnetworks.facebook',
            'socialnetworks.github',
            'socialnetworks.linkedin',
            'socialnetworks.moves',
            'socialnetworks.paypal',
            'socialnetworks.twitter',
        ),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        AUTHENTICATION_BACKENDS=(
            'django.contrib.auth.backends.ModelBackend',
            'socialnetworks.facebook.backends.FacebookBackend',
            'socialnetworks.github.backends.GitHubBackend',
            'socialnetworks.linkedin.backends.LinkedInBackend',
            'socialnetworks.moves.backends.MovesAppBackend',
            'socialnetworks.paypal.backends.PayPalBackend',
            'socialnetworks.twitter.backends.TwitterBackend',
        ),
        ROOT_URLCONF='tests.urls',
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        SOCIALNETWORKS_CONFIGURATION={
            'FACEBOOK': {
                'APP_ID': 'test-facebook-app',
                'APP_SECRET': 'test-facebook-secret',
            },
            'GITHUB': {
                'APP_ID': 'test-github-app',
                'APP_SECRET': 'test-github-secret',
            },
            'LINKEDIN': {
                'APP_ID': 'test-linkedin-app',
                'APP_SECRET': 'test-linkedin-secret',
            },
            'MOVES_APP': {
                'APP_ID': 'test-moves-app',
                'APP_SECRET': 'test-moves-secret',
            },
            'PAYPAL': {
                'APP_ID': 'test-paypal-app',
                'APP_SECRET': 'test-paypal-secret',
                'IS_LIVE': False,
            },
            'TWITTER': {
                'APP_ID': 'test-twitter-app',
                'APP_SECRET': 'test-twitter-secret',
            },
        }
    )
