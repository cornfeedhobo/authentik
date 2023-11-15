# Generated by Django 4.2.7 on 2023-11-15 10:53

import uuid

import django.db.models.deletion
import django_tenants.postgresql_backend.base
from django.db import migrations, models

from authentik.lib.config import CONFIG


def create_default_tenant(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Tenant = apps.get_model("authentik_tenants", "Tenant")
    tenant = Tenant.objects.using(db_alias).create(
        schema_name="public",
        name="Default",
        ready=True,
        avatars=CONFIG.get("avatars", "gravatar,initials"),
        default_user_change_name=CONFIG.get_bool("default_user_change_name", True),
        default_user_change_email=CONFIG.get_bool("default_user_change_email", False),
        default_user_change_username=CONFIG.get_bool("default_user_change_username", False),
        gdpr_compliance=CONFIG.get_bool("gdpr_compliance", True),
        impersonation=CONFIG.get_bool("impersonation", True),
        footer_links=CONFIG.get("footer_links", default=[]),
    )

    Domain = apps.get_model("authentik_tenants", "Domain")
    domain = Domain.objects.using(db_alias).create(domain="*", tenant=tenant, is_primary=True)


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tenant",
            fields=[
                (
                    "schema_name",
                    models.CharField(
                        db_index=True,
                        max_length=63,
                        unique=True,
                        validators=[django_tenants.postgresql_backend.base._check_schema_name],
                    ),
                ),
                (
                    "tenant_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.TextField()),
                ("ready", models.BooleanField(default=False)),
                (
                    "avatars",
                    models.TextField(
                        default="gravatar,initials",
                        help_text="Configure how authentik should show avatars for users.",
                    ),
                ),
                (
                    "default_user_change_name",
                    models.BooleanField(
                        default=True, help_text="Enable the ability for users to change their name."
                    ),
                ),
                (
                    "default_user_change_email",
                    models.BooleanField(
                        default=False,
                        help_text="Enable the ability for users to change their email address.",
                    ),
                ),
                (
                    "default_user_change_username",
                    models.BooleanField(
                        default=False,
                        help_text="Enable the ability for users to change their username.",
                    ),
                ),
                (
                    "gdpr_compliance",
                    models.BooleanField(
                        default=True,
                        help_text="When enabled, all the events caused by a user will be deleted upon the user's deletion.",
                    ),
                ),
                (
                    "impersonation",
                    models.BooleanField(
                        default=True, help_text="Globally enable/disable impersonation."
                    ),
                ),
                (
                    "footer_links",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="The option configures the footer links on the flow executor pages.",
                    ),
                ),
                (
                    "reputation_expiry",
                    models.PositiveBigIntegerField(
                        default=86400,
                        help_text="Configure how long reputation scores should be saved for in seconds.",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tenant",
                "verbose_name_plural": "Tenants",
            },
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("domain", models.CharField(db_index=True, max_length=253, unique=True)),
                ("is_primary", models.BooleanField(db_index=True, default=True)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domains",
                        to="authentik_tenants.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Domain",
                "verbose_name_plural": "Domains",
            },
        ),
        migrations.RunPython(code=create_default_tenant, reverse_code=migrations.RunPython.noop),
    ]
