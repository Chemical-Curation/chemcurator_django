import json

import requests
from config.settings import RESOLUTION_SUBSTANCE_URI, RESOLUTION_URL


class SubstanceIndex:
    substance_url = f"{RESOLUTION_URL}{RESOLUTION_SUBSTANCE_URI}"

    def index(self, substance):
        headers = {"Content-Type": "application/vnd.api+json"}
        data = json.dumps(
            {
                "id": substance.sid,
                "identifiers": {
                    "preferred_name": substance.preferred_name,
                    "display_name": substance.display_name,
                    "casrn": substance.casrn,
                    "synonyms": [
                        {"identifier": synonym.identifier}
                        for synonym in substance.synonym_set.all()
                    ],
                },
            }
        )
        requests.post(self.substance_url, data, headers=headers)
