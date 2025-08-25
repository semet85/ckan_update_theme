import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import BaseController, render
from ckan import model


class InsightController(BaseController):

    def index(self):
        # Ambil semua group yang punya tag "insight"
        groups = (
            model.Session.query(model.Group)
            .filter(model.Group.state == "active")
            .join(model.tag_table, model.Group.tags)
            .filter(model.tag_table.c.name == "insight")
            .all()
        )

        context = {"groups": groups}
        return render("insight/index.html", extra_vars=context)


class DatopianPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")
        toolkit.add_resource("fanstatic", "datopian")

    def before_map(self, map):
        map.connect(
            "insight",
            "/insight",
            controller="ckanext.datopian.plugin:InsightController",
            action="index",
        )
        return map
