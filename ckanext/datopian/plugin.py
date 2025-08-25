import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template
from ckan import model


insight_blueprint = Blueprint(
    "insight", __name__
)


@insight_blueprint.route("/insight")
def insight_index():
    # ambil group dengan tag "insight"
    groups = (
        model.Session.query(model.Group)
        .filter(model.Group.state == "active")
        .join(model.group_tag_table)
        .join(model.tag_table)
        .filter(model.tag_table.c.name == "insight")
        .all()
    )
    return render_template("insight/index.html", groups=groups)


class DatopianPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")
        toolkit.add_resource("fanstatic", "datopian")

    def get_blueprint(self):
        return [insight_blueprint]
