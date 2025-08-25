from ckan.plugins import SingletonPlugin, implements, IConfigurer, IBlueprint
import ckan.plugins.toolkit as toolkit
from flask import Blueprint, render_template
from ckan import model

# Blueprint untuk halaman /insight
insight_blueprint = Blueprint(
    'datopian_insight',        # nama blueprint unik
    __name__,
    template_folder='templates'
)

@insight_blueprint.route("/insight", endpoint="datopian_insight_index")
def insight_index():
    """Tampilkan semua group yang punya extras['insight']='true'"""
    groups = (
        model.Session.query(model.Group)
        .filter(model.Group.state == "active")
        .filter(model.Group.extras.any(key="insight", value="true"))
        .all()
    )
    return render_template("insight/index.html", groups=groups)

# Plugin CKAN
class DatopianPlugin(SingletonPlugin):
    implements(IConfigurer)
    implements(IBlueprint)

    def update_config(self, config):
        # Tambahkan template dan public folder
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")
        toolkit.add_resource("fanstatic", "datopian")

    def get_blueprint(self):
        # Kembalikan blueprint
        return [insight_blueprint]


    def get_commands(self):
        from . import commands
        return [commands.insight]
    
    @insight_blueprint.route("/insight", endpoint="datopian_insight_index")
    def insight_index():
        groups = (
            model.Session.query(model.Group)
            .filter(model.Group.state == "active")
            .filter(model.Group.extras.any(key="insight", value="true"))
            .all()
    )
        return render_template("insight/index.html", groups=groups)

