import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base

class InsightController(base.BaseController):

    def index(self):
        query = toolkit.request.params.get('q', '')
        all_groups = toolkit.get_action('group_list')(
            context={'model': toolkit.model, 'session': toolkit.model.Session, 'user': toolkit.c.user},
            data_dict={}
        )

        insight_groups = []
        for g in all_groups:
            group_detail = toolkit.get_action('group_show')(
                context={'model': toolkit.model, 'session': toolkit.model.Session, 'user': toolkit.c.user},
                data_dict={'id': g['id']}
            )
            if 'insight' in [t['name'] for t in group_detail['tags']]:
                if not query or query.lower() in group_detail['name'].lower() or query.lower() in group_detail.get('description', '').lower():
                    insight_groups.append(group_detail)

        c = toolkit.c
        c.page = type('obj', (), {})()
        c.page.items = insight_groups
        c.page.pager = lambda: ''
        c.page.search_query = query

        return base.render('insight/index.html')

    def read(self, id):
        group_detail = toolkit.get_action('group_show')(
            context={'model': toolkit.model, 'session': toolkit.model.Session, 'user': toolkit.c.user},
            data_dict={'id': id}
        )
        if 'insight' not in [t['name'] for t in group_detail['tags']]:
            return base.abort(404)

        c = toolkit.c
        c.group_dict = group_detail
        return base.render('insight/read.html')
