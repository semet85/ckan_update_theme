import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .blueprints import insight  # ambil blueprint


def hello_plugin():
    return u'Hello from the Datopian Theme extension'


class DatopianPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
                             'datopian')

    # IBlueprint

    def get_blueprint(self):
         # Daftarkan blueprint insight
        return [insight.blueprint]
