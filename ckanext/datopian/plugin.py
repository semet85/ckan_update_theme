import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template
from ckan import model

# Blueprint untuk route /insight
insight_blueprint = Blueprint(
    "insight", __name__
)

@insight_blueprint.route("/insight")
def insight_index():
    # Ambil semua group dengan extras insight=true
    groups = (
        model.Session.query(model.Group)
        .filter(model.Group.state == "active")
        .filter(model.Group.extras.any(key="insight", value="true"))
        .all()
    )
    return render_template("insight/index.html", groups=groups)


class DatopianPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config):
        # Daftarkan template & public folder
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")
        toolkit.add_resource("fanstatic", "datopian")

    def get_blueprint(self):
        # Kembalikan blueprint untuk CKAN
        return [insight_blueprint]
