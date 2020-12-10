# Generated by Django 1.10.7 on 2017-08-11 15:08


from django.db import migrations, models

from zds.utils.models import Tag


def force_unicity(*args, **kwargs):
    duplicates = (
        Tag.objects.values("slug")
        .order_by()
        .annotate(min_id=models.Min("id"), count_occurrences=models.Count("id"))
        .filter(count_occurrences__gt=1)
    )

    for duplicate in duplicates:
        print(
            '\n   - Altering duplicates for slug "{}" ({} occurrences)'.format(
                duplicate["slug"], duplicate["count_occurrences"]
            ),
            end="",
        )

        duplicates_to_modify = Tag.objects.filter(slug=duplicate["slug"]).exclude(id=duplicate["min_id"])

        for duplicate_to_modify in duplicates_to_modify:
            duplicate_to_modify.save()  # will change the slug automatically, due to the use of uuslug


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0012_commentedit"),
    ]

    operations = [
        migrations.RunPython(force_unicity),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(max_length=30, unique=True, verbose_name="Slug"),
        ),
        migrations.AlterField(
            model_name="category",
            name="position",
            field=models.IntegerField(db_index=True, default=0, verbose_name="Position"),
        ),
    ]
