import ckan.plugins.toolkit as toolkit
import ckan.model as model
from flask import Blueprint, request, render_template

blueprint = Blueprint(
    "insight", __name__,
    url_prefix="/insight",
    template_folder="../../templates"
)

@blueprint.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")

    context = {
        "model": model,
        "session": model.Session,
        "user": toolkit.g.user or ""
    }

    all_groups = toolkit.get_action("group_list")(
        context=context,
        data_dict={}
    )

    insight_groups = []
    for g in all_groups:   # g = string nama group
        group_detail = toolkit.get_action("group_show")(
            context=context,
            data_dict={"id": g}
        )
        if "insight" in [t["name"] for t in group_detail["tags"]]:
            if not query or query.lower() in group_detail["name"].lower() or query.lower() in group_detail.get("description", "").lower():
                insight_groups.append(group_detail)

    page = type("obj", (), {})()
    page.items = insight_groups
    page.pager = lambda: ""
    page.search_query = query

    return render_template("insight/index.html", page=page)



@blueprint.route("/<id>", methods=["GET"])
def read(id):
    context = {
        "model": model,
        "session": model.Session,
        "user": toolkit.g.user or ""
    }

    group_detail = toolkit.get_action("group_show")(
        context=context,
        data_dict={"id": id}
    )
    if "insight" not in [t["name"] for t in group_detail["tags"]]:
        return toolkit.abort(404)

    return render_template("insight/read.html", group=group_detail)

blueprint = Blueprint("datopian_insight", __name__)

@blueprint.route("/insight")
def index():
    context = {"user": toolkit.g.user}
    # ambil semua group yang punya tag insight
    groups = toolkit.get_action("group_list")(
        context, {"all_fields": True}
    )
    insights = [g for g in groups if "insight" in [t["name"] for t in g.get("tags", [])]]

    return render_template("insight/index.html", groups=insights)