import flask
import flask_cors
import cache
import cache.key
import login
import login.apps
import login.utils
import tool_api
import resources
import service
import service.members
import species_trie.apps
import summary
import summary.apps
from src import model
from src import config

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
app.config["JWT_SECRET_KEY"] = config.get_file_content(config.EnvKeys.JWT_SECRET)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get_jwt_access_token_expires()
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["CACHE_TYPE"] = config.get_cache_type()
app.config["CACHE_KEY_PREFIX"] = config.get_env(config.EnvKeys.CACHE_KEY_PREFIX)
app.config["CACHE_REDIS_HOST"] = config.get_env(config.EnvKeys.CACHE_REDIS_HOST)
app.config["CACHE_REDIS_PORT"] = config.get_env(config.EnvKeys.CACHE_REDIS_PORT)

flask_cors.CORS(app)
# flask_cors.CORS(
#     app,
#     resources={
#         r"/*": {"origins": config.get_env(config.EnvKeys.ACCESS_CONTROL_ALLOW_ORIGIN)}
#     },
#     supports_credentials=True,
#     allow_headers="*",
# )


resources.api.init_resources()
resources.api.init_app(app)
tool_api.api.init_resources()
tool_api.api.init_app(app)
summary.api.init_resources()
summary.api.init_app(app)
login.jwt.init_app(app)
model.db.init_app(app)
model.migrate.init_app(app, model.db)
cache.cache.init_app(app)

app.register_blueprint(login.apps.blueprint)
app.register_blueprint(species_trie.apps.blueprint)
app.register_blueprint(summary.apps.blueprint)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/_clear_cache/<string:group>")
def clear_cache(group: str):
    cache.key.evict_group_cache(group)


if __name__ == "__main__":
    cache.cache.clear()
    app.run(host="127.0.0.1", debug=True)
