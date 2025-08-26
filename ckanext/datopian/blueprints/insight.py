import ckan.plugins.toolkit as toolkit
import ckan.model as model
from flask import Blueprint, request, render_template

blueprint = Blueprint(
    "datopian_insight", __name__,
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
        data_dict={"all_fields": True}
    )

    insight_groups = []
    for g in all_groups:
        if "insight" in [t["name"] for t in g.get("tags", [])]:
            if not query or query.lower() in g["name"].lower() or query.lower() in g.get("description", "").lower():
                insight_groups.append(g)

    # supaya template bisa akses langsung groups
    return render_template(
        "insight/index.html",
        groups=insight_groups,
        context=context,
        query=query
    )


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

    return render_template("insight/read.html", group=group_detail, context=context)
