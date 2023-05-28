# Sample GraphQL server with Flask, Ariadne and SQLAlchemy

A sample python server app I wrote when I was learning about the **GraphQL**.


# About this sample

This sample app has three key componets:

* `flask` a micro web framework for Python
* `SQLAlchemy` a Python SQL toolkit and Object Relational Mapper
* `Ariadne` a schema-first Python library for implementing GraphQL servers


The app and its code is meant to be simple, yet still follow current
best practices for the aforementioned components.

* SQLAlchemy Models are defined declaratively and without `Flask-SQLAlchemy`
    * https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5508
    * https://flask.palletsprojects.com/en/2.3.x/patterns/sqlalchemy/#declarative
* `backref` Relationships API used for many-to-many mappings
    * https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref
    * https://docs.sqlalchemy.org/en/20/orm/relationship_api.html
    * https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
* Select construct used instead of legacy query API
    * https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5159
    * https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
    * https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query
* Uses GraphiQL 2 instead of deprecated GraphQL Playground
    * https://ariadnegraphql.org/docs/explorers
* GraphQL schema is loaded from a dir instead of file which allows for modularization (although it's not really used here)
    * https://ariadnegraphql.org/docs/modularization
* GraphQL schema documented via descriptions (even using Markdown)
    * https://ariadnegraphql.org/docs/documenting-schema


## Back-end database

Data source used by the app is a Sakila DB in sqlite3 format:
https://github.com/ivanceras/sakila/tree/master
ER diagram of the DB is available here:
https://www.kaggle.com/datasets/atanaskanev/sqlite-sakila-sample-database?select=SQLite3+Sakila+Sample+Database+ERD.png


# Run localy

    python ./run.py

or

    export FLASK_APP=run.py && flask run --reload

and then access:

    http://127.0.0.1:5000


# TODO

* Flask application in packages (blueprints)
 * https://flask.palletsprojects.com/en/2.3.x/patterns/packages/
* Package management via pyproject.toml
 * https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
* Anotations
 * https://peps.python.org/pep-0484/
 * https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
* Add tox.ini
* Add Yamlint
* Use mapped_column and annotations for the fields


# Example of GraphGL queries

## listFilms

    query {
      listFilms {
          success
          errors
          data {
            film_id
            title
            description
        }
      }
    }

## getFilm

    query {
      getFilm(film_id: 3) {
        success
        errors
        data {
          film_id
          title
          description
          actors {
            actor_id
            first_name
            last_name
          }
          categories {
            category_id
            name
            last_update
          }
        }
      }
    }

## searchFilms

    query {
      searchFilms(title: "apache") {
        success
        errors
        data {
          film_id
          title
          description
          actors {
            actor_id
            first_name
            last_name
          }
          categories {
            category_id
            name
            last_update
          }
        }
      }
    }


# Dev setup

**Create a virtual environment by Virtualenv**

    $ mkvirtualenv graphql-sample

**Use the virtual environment**

    $ workon graphql-sample

**Install deps**

    $ pip3 install -r requirements.txt
