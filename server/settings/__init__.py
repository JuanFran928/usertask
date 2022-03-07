import environ

from server.env import env

environ.Env.read_env()

app_stage = env("DJANGO_APP_STAGE") 

if app_stage == 'prod':
    from .prod import *
else:
    from .dev import *