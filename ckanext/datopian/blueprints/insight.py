import ckan.plugins.toolkit as toolkit
from flask import Blueprint, request, render_template

blueprint = Blueprint(
    "insight", __name__,
    url_prefix="/insight",
    template_folder="../../templates"
)

@blueprint.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")

    all_groups = toolkit.get_action("group_list")(
        context={"model": toolkit.model, "session": toolkit.model.Session, "user": toolkit.c.user},
        data_dict={}
    )

    insight_groups = []
    for g in all_groups:
        group_detail = toolkit.get_action("group_show")(
            context={"model": toolkit.model, "session": toolkit.model.Session, "user": toolkit.c.user},
            data_dict={"id": g["id"]}
        )
        if "insight" in [t["name"] for t in group_detail["tags"]]:
            if not query or query.lower() in group_detail["name"].lower() or query.lower() in group_detail.get("description", "").lower():
                insight_groups.append(group_detail)

    c = toolkit.c
    c.page = type("obj", (), {})()
    c.page.items = insight_groups
    c.page.pager = lambda: ""
    c.page.search_query = query

    return render_template("insight/index.html")


@blueprint.route("/<id>", methods=["GET"])
def read(id):
    group_detail = toolkit.get_action("group_show")(
        context={"model": toolkit.model, "session": toolkit.model.Session, "user": toolkit.c.user},
        data_dict={"id": id}
    )
    if "insight" not in [t["name"] for t in group_detail["tags"]]:
        return toolkit.abort(404)

    c = toolkit.c
    c.group_dict = group_detail
    return render_template("insight/read.html")
