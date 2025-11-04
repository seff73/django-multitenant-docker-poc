from django.core.management.base import BaseCommand, CommandError
from tenancy.models import Client, Domain


class Command(BaseCommand):
    help = "Provision a new tenant: creates schema and sets primary domain."

    def add_arguments(self, parser):
        parser.add_argument("--schema", required=True, help="Schema name (e.g., clinic_a)")
        parser.add_argument("--domain", required=True, help="Primary domain (e.g., clinic-a.localtest.me)")
        parser.add_argument("--name", default=None, help="Optional display name")

    def handle(self, *args, **options):
        schema = options["schema"].strip()
        domain = options["domain"].strip()
        name = options["name"] or schema

        if schema == "public":
            raise CommandError("Schema name 'public' is reserved.")

        if Client.objects.filter(schema_name=schema).exists():
            raise CommandError(f"Client with schema '{schema}' already exists")

        client = Client(schema_name=schema, name=name)
        client.save()  # auto_create_schema will create schema and run tenant migrations

        Domain.objects.create(domain=domain, tenant=client, is_primary=True)
        self.stdout.write(self.style.SUCCESS(f"Tenant created: schema={schema}, domain={domain}"))
