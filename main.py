from flask import Flask, render_template

from app.core.config import config
from app.core.database import Database
from app.core.container import Container
from app.models.animal import Animal

app = Flask(
    __name__,
    template_folder=config.paths.FRONTEND_DIR / "templates",
    static_folder=config.paths.FRONTEND_DIR / "static",
)

database = Database(config.database.database_url())
container = Container(database.get_db())
animal_servise = container.get_animal_service()


@app.route("/")
def animals():
    animals = animal_servise.get_animals()
    return render_template("index.html", animals=animals)


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
