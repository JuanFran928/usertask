from server.settings.env import env

env.read_env()

app_stage = env("DJANGO_APP_STAGE") 

if app_stage == 'prod':
    from .prod import *
else:
    from .dev import *