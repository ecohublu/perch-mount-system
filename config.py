import app.env


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s:%s/%s" % (
        app.env.get_env(app.env.EnvKeys.POSTGRESQL_USER),
        app.env.get_env(app.env.EnvKeys.POSTGRESQL_PASSWORD),
        app.env.get_env(app.env.EnvKeys.POSTGRESQL_HOST),
        app.env.get_env(app.env.EnvKeys.POSTGRESQL_PORT),
        app.env.get_env(app.env.EnvKeys.POSTGRESQL_DATABASE_NAME),
    )
    SECRET_KEY = app.env.get_file_content(app.env.EnvKeys.FLASK_SECRET)
    JWT_SECRET_KEY = app.env.get_file_content(app.env.EnvKeys.JWT_SECRET)
    JWT_ACCESS_TOKEN_EXPIRES = app.env.get_jwt_access_token_expires()
    PROPAGATE_EXCEPTIONS = True
