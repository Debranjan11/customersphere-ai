from backend.core import settings

print(settings.app.app_name)

print(settings.app.app_version)

print(settings.database.database_url)

print(settings.security.secret_key)

print(settings.security.algorithm)