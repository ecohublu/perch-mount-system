import datetime
import flask
from tool_api.service import sections

blueprint = flask.Blueprint("tool_api", __name__)

blueprint.route("/shift_time", methods=["PATCH"])


def shift_time():
    args = flask.request.args
    if not args["section_id"] or args["start_time"]:
        return flask.jsonify({"message: section_id and start_time is required"}, 400)

    sections.shift_datetimes(int(args["section_id"]))
    return
