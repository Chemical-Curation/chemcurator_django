from rest_framework.exceptions import ParseError

from rest_framework_json_api import exceptions, parsers, serializers, utils


class JSONParser(parsers.JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        """Slightly modified to also check DELETE request body data _if_ provided."""

        result = super(parsers.JSONParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context
        )
        if not isinstance(result, dict) or "data" not in result:
            raise ParseError("Received document does not contain primary data")

        data = result.get("data")
        view = parser_context["view"]

        from rest_framework_json_api.views import RelationshipView

        if isinstance(view, RelationshipView):
            # We skip parsing the object as JSONAPI Resource Identifier Object and not a regular
            # Resource Object
            if isinstance(data, list):
                for resource_identifier_object in data:
                    if not (
                        resource_identifier_object.get("id")
                        and resource_identifier_object.get("type")
                    ):
                        raise ParseError(
                            "Received data contains one or more malformed JSONAPI "
                            "Resource Identifier Object(s)"
                        )
            elif not (data.get("id") and data.get("type")):
                raise ParseError(
                    "Received data is not a valid JSONAPI Resource Identifier Object"
                )

            return data

        request = parser_context.get("request")

        # Sanity check
        if not isinstance(data, dict):
            raise ParseError(
                "Received data is not a valid JSONAPI Resource Identifier Object"
            )

        # Check for inconsistencies
        if request.method in ("PUT", "POST", "PATCH", "DELETE"):
            resource_name = utils.get_resource_name(
                parser_context, expand_polymorphic_types=True
            )
            if isinstance(resource_name, str):
                if data.get("type") != resource_name:
                    raise exceptions.Conflict(
                        "The resource object's type ({data_type}) is not the type that "
                        "constitute the collection represented by the endpoint "
                        "({resource_type}).".format(
                            data_type=data.get("type"), resource_type=resource_name
                        )
                    )
            else:
                if data.get("type") not in resource_name:
                    raise exceptions.Conflict(
                        "The resource object's type ({data_type}) is not the type that "
                        "constitute the collection represented by the endpoint "
                        "(one of [{resource_types}]).".format(
                            data_type=data.get("type"),
                            resource_types=", ".join(resource_name),
                        )
                    )
        if not data.get("id") and request.method in ("PATCH", "PUT", "DELETE"):
            raise ParseError(
                "The resource identifier object must contain an 'id' member"
            )

        if request.method in ("PATCH", "PUT", "DELETE"):
            lookup_url_kwarg = getattr(view, "lookup_url_kwarg", None) or getattr(
                view, "lookup_field", None
            )
            if lookup_url_kwarg and str(data.get("id")) != str(
                view.kwargs[lookup_url_kwarg]
            ):
                raise exceptions.Conflict(
                    "The resource object's id ({data_id}) does not match url's "
                    "lookup id ({url_id})".format(
                        data_id=data.get("id"), url_id=view.kwargs[lookup_url_kwarg]
                    )
                )

        # Construct the return data
        serializer_class = getattr(view, "serializer_class", None)
        parsed_data = {"id": data.get("id")} if "id" in data else {}
        # `type` field needs to be allowed in none polymorphic serializers
        if serializer_class is not None:
            if issubclass(serializer_class, serializers.PolymorphicModelSerializer):
                parsed_data["type"] = data.get("type")
        parsed_data.update(self.parse_attributes(data))
        parsed_data.update(self.parse_relationships(data))
        parsed_data.update(self.parse_metadata(result))
        return parsed_data
