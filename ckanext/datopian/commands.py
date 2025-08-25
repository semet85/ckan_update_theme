import click
import ckan.plugins.toolkit as toolkit
from ckan import model

@click.group()
def insight():
    """Manage Insight extras for groups."""
    pass

@insight.command()
@click.argument("group_names", nargs=-1)
def add(group_names):
    """
    Tambahkan extras 'insight=true' ke satu atau lebih group.
    Contoh: ckan insight add ekonomi pendidikan kesehatan
    """
    for name in group_names:
        group = model.Group.get(name)
        if not group:
            click.echo(f"Group '{name}' tidak ditemukan")
            continue

        existing = {e.key: e.value for e in group.extras}
        if existing.get("insight") == "true":
            click.echo(f"Group '{name}' sudah punya extras insight=true")
            continue

        group.extras.append(model.GroupExtra(group_id=group.id, key="insight", value="true"))
        model.Session.add(group)
        click.echo(f"Group '{name}' ditandai sebagai Insight")

    model.Session.commit()
    click.echo("Selesai menambahkan extras Insight")

@insight.command()
@click.argument("group_names", nargs=-1)
def remove(group_names):
    """
    Hapus extras 'insight' dari satu atau lebih group.
    Contoh: ckan insight remove ekonomi pendidikan
    """
    for name in group_names:
        group = model.Group.get(name)
        if not group:
            click.echo(f"Group '{name}' tidak ditemukan")
            continue

        # Hapus extras insight
        to_delete = [e for e in group.extras if e.key == "insight"]
        if not to_delete:
            click.echo(f"Group '{name}' tidak punya extras insight")
            continue

        for e in to_delete:
            model.Session.delete(e)

        click.echo(f"Extras Insight di group '{name}' dihapus")

    model.Session.commit()
    click.echo("Selesai menghapus extras Insight")
