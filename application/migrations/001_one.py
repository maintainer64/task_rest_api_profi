"""Peewee migrations -- 001_one.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext  # noqa: F401
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class PromoDB(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(index=True, max_length=255)
        description = pw.CharField(index=True, max_length=255, null=True)

        class Meta:
            table_name = "promo"

    @migrator.create_model
    class MemberDB(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(index=True, max_length=255)
        promo = pw.ForeignKeyField(
            backref="members", column_name="promo_id", field="id", model=migrator.orm["promo"], on_delete="CASCADE"
        )

        class Meta:
            table_name = "member"

    @migrator.create_model
    class PrizeDB(pw.Model):
        id = pw.AutoField()
        description = pw.CharField(index=True, max_length=255)
        promo = pw.ForeignKeyField(
            backref="prizes", column_name="promo_id", field="id", model=migrator.orm["promo"], on_delete="CASCADE"
        )

        class Meta:
            table_name = "prize"


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model("promo")

    migrator.remove_model("prize")

    migrator.remove_model("member")