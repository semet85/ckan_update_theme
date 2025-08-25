import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class DatopianPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    def update_config(self, config):
        # Tambahkan path template & public
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def before_map(self, map):
        controller = 'ckanext.datopian.controllers.insight:InsightController'
        map.connect('insight_index', '/insight',
                    controller=controller, action='index')
        map.connect('insight_read', '/insight/{id}',
                    controller=controller, action='read')
        return map

    def after_map(self, map):
        return map
