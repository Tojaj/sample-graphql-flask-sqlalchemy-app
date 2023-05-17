from flask import Flask, request, redirect, jsonify, url_for
from flask_cors import CORS

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
)
from ariadne.explorer import ExplorerPlayground
from ariadne.explorer import ExplorerGraphiQL

from app.database import db_session
from app.queries import listFilms_resolver, getFilm_resolver, searchFilms_resolver

query = ObjectType("Query")
query.set_field("listFilms", listFilms_resolver)
query.set_field("getFilm", getFilm_resolver)
query.set_field("searchFilms", searchFilms_resolver)

type_defs = load_schema_from_path("schema/")
schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return redirect(url_for("graphql_explorer"))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


explorer_html = ExplorerGraphiQL().html(None)


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code
