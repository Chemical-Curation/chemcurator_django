import json

import requests
from config.settings import RESOLUTION_URL


class Index:
    """ChemCurator to interface with the resolver app.
    """

    HEADERS = {"Content-Type": "application/vnd.api+json"}

    def __init__(self, fail_silently=True):
        self.fail_silently = fail_silently

        for attr in ["index_url", "delete_url", "delete_pk"]:
            assert getattr(
                self, attr
            ), "Class {index_class} missing {attr} attribute".format(
                index_class=self.__class__.__name__, attr=attr
            )

    def sync_instances(self, instances, delete=False):
        """Posts instance(s) to resolver.

        Args:
            instances (`list` of `:obj:` or :obj:): model instances to be saved in resolver
            delete (bool): Whether this will add or remove the instance
        """
        try:  # Attempt to iterate instances
            for instance in instances:
                self._sync_instance(instance, delete)
        except TypeError:  # Assume solo instance
            self._sync_instance(instances, delete)

    def _sync_instance(self, instance, delete):
        """Handles the posting of an instance to resolver.

        Args:
            instance (:obj:Substance): Substances to be saved in resolver
        """
        #  add the instance
        if not delete:
            model_document = self.get_model_document(instance)
            data = json.dumps(model_document)
            try:
                requests.post(self.index_url, data, headers=self.HEADERS)
            except requests.exceptions.ConnectionError as conn_err:
                if not self.fail_silently:
                    raise conn_err
        # remove the instance
        else:
            try:
                requests.delete(
                    self.delete_url + getattr(instance, self.delete_pk),
                    headers=self.HEADERS,
                )
            except requests.exceptions.ConnectionError as conn_err:
                if not self.fail_silently:
                    raise conn_err

    def delete_all_instances(self):
        try:
            requests.delete(self.index_url, headers=self.HEADERS)
        except requests.exceptions.ConnectionError as conn_err:
            if not self.fail_silently:
                raise conn_err

    def get_model_document(self, instance):
        raise NotImplementedError("`get_model_document()` must be implemented.")


class SubstanceIndex(Index):
    index_url = f"{RESOLUTION_URL}/api/v1/substances/_index"
    delete_url = f"{RESOLUTION_URL}/api/v1/substances/"
    delete_pk = "sid"

    def get_model_document(self, instance):
        return {
            "data": {
                "id": instance.sid,
                "type": "substance",
                "attributes": {
                    "identifiers": {
                        "preferred_name": instance.preferred_name,
                        "display_name": instance.display_name,
                        "casrn": instance.casrn,
                        "synonyms": [
                            {"identifier": synonym.identifier}
                            for synonym in instance.synonym_set.all()
                        ],
                    },
                },
            }
        }
