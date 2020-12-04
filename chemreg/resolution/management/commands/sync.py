from django.apps import apps
from django.core.management import BaseCommand

import requests

from chemreg.resolution.indices import SubstanceIndex


class Command(BaseCommand):
    help = "Syncs chemcurator models with resolver"

    def handle(self, *args, **options):
        # I'm stealing the migrate heading because it looks good.
        self.stdout.write(
            self.style.MIGRATE_HEADING("Syncing Substances with Resolver")
        )

        try:
            self.sync_substances()
        except requests.exceptions.ConnectionError as conn_err:
            self.stderr.write(str(conn_err))
        except Exception as e:
            self.stderr.write(str(e))
        else:
            self.stdout.write(self.style.SUCCESS("Substances Synced"))

    def sync_substances(self):
        substance_index = SubstanceIndex(fail_silently=False)

        # Delete existing index
        self.stdout.write("Clearing substances... ")
        substance_index.delete_all_instances()
        self.stdout.write(self.style.SUCCESS("Done"))

        # Loop through all substances and post.
        sub_count = apps.get_model("substance.Substance").objects.count()
        self.stdout.write(f"Updating {sub_count} substances... ")

        substance_index.sync_instances(
            apps.get_model("substance.Substance").objects.all()
        )

        self.stdout.write(self.style.SUCCESS("Done"))
