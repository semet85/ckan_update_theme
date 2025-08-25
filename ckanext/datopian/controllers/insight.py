import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import ckan.model as model

log = __import__('logging').getLogger(__name__)

class InsightController(base.BaseController):
    def index(self):
        query = toolkit.request.params.get('q', '')  # ambil query search
        groups = model.Session.query(model.Group).all()
        
        # filter hanya group dengan tag 'insight'
        insight_groups = [g for g in groups if 'insight' in [t.name for t in g.tags]]
        
        if query:
            # filter sesuai nama/deskripsi
            insight_groups = [g for g in insight_groups if query.lower() in g.name.lower() or
                              (g.description and query.lower() in g.description.lower())]

        c = toolkit.c
        c.page = type('obj', (), {})()
        c.page.items = insight_groups
        c.page.pager = lambda: ''  # bisa ditambah pager CKAN
        c.page.search_query = query

        return base.render('insight/index.html')

    def read(self, id):
        group = model.Group.get(id)
        if not group or 'insight' not in [t.name for t in group.tags]:
            return base.abort(404)

        c = toolkit.c
        c.group_dict = toolkit.get_action('group_show')(
            {'model': model, 'session': model.Session, 'user': toolkit.c.user},
            {'id': group.id}
        )
        return base.render('insight/read.html')
