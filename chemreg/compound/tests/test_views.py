from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from chemreg.compound.models import DefinedCompound
from chemreg.compound.tests.factories import DefinedCompoundFactory


class TestDefinedCompoundViewSet(APITestCase):
    def setUp(self):
        self.dc = DefinedCompoundFactory()
        self.list_url = reverse("definedcompound-list")
        self.detail_url = reverse("definedcompound-detail", kwargs={"cid": self.dc.cid})
        self.paginated_url = f"{self.list_url}?size=5&page=2"

    def test_meta_response(self):
        response = self.client.get(self.list_url, content_type="application/json")
        got = response.json()
        expected = {"totalPages": 1, "page_size": 100, "apiVersion": "1.0.0-beta"}
        self.assertEqual(got["meta"], expected)

    def test_links_response(self):
        response = self.client.get(self.list_url, content_type="application/json")
        got = response.json()
        expected = {
            "self": "http://testserver/defined-compounds/?page=1",
            "first": "http://testserver/defined-compounds/?page=1",
            "previous": None,
            "next": None,
            "last": "http://testserver/defined-compounds/?page=1",
        }
        self.assertEqual(got["links"], expected)

    def test_list_view(self):
        response = self.client.get(self.list_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DefinedCompound.objects.count(), len(response.data["data"]))
        got = response.json()
        expected = [
            {
                "type": "defined compound",
                "id": self.dc.cid,
                "attributes": {
                    "molfile-v3000": self.dc.molefile,
                    "inchikey": self.dc.inchikey,
                },
            }
        ]
        self.maxDiff = None
        self.assertEqual(got["data"], expected)

    def test_pagination(self):
        dcs = {}
        for i in range(0, 19):
            dcs[i] = DefinedCompoundFactory()
        response = self.client.get(self.paginated_url, content_type="application/json")
        got = response.json()
        expected = {
            "self": "http://testserver/defined-compounds/?page=2&size=5",
            "first": "http://testserver/defined-compounds/?page=1&size=5",
            "previous": "http://testserver/defined-compounds/?size=5",
            "next": "http://testserver/defined-compounds/?page=3&size=5",
            "last": "http://testserver/defined-compounds/?page=4&size=5",
        }
        self.assertEqual(got["links"], expected)

    def test_create_view(self):
        new = {"molefile": "new mole", "inchikey": "ADVPTQAUNPRNPO-UHFFFAOYSA-N"}
        response = self.client.post(self.list_url, new)
        assert response.status_code == 201
        new = DefinedCompound.objects.last()
        assert response.data["id"]
        assert new.cid == response.data["id"]
        assert new.molefile == response.data["attributes"]["molfile-v3000"]
        assert new.inchikey == response.data["attributes"]["inchikey"]

    def test_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("attributes", response.data)
        self.assertEqual(self.dc.cid, response.data["id"])
        self.assertEqual(self.dc.molefile, response.data["attributes"]["molfile-v3000"])
        self.assertEqual(self.dc.inchikey, response.data["attributes"]["inchikey"])

    def test_destroy_view(self):
        response = self.client.delete(self.detail_url)
        assert response.status_code == 204
