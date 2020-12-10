from collections import OrderedDict, defaultdict

from rest_framework_json_api import renderers, utils

from chemreg.jsonapi.serializers import PolymorphicModelSerializer


class JSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Slightly modified to accept our modified PolymorphicSerializer."""

        renderer_context = renderer_context or {}

        view = renderer_context.get("view", None)
        request = renderer_context.get("request", None)

        # Get the resource name.
        resource_name = utils.get_resource_name(renderer_context)

        # If this is an error response, skip the rest.
        if resource_name == "errors":
            return self.render_errors(data, accepted_media_type, renderer_context)

        # if response.status_code is 204 then the data to be rendered must
        # be None
        response = renderer_context.get("response", None)
        if response is not None and response.status_code == 204:
            return super(JSONRenderer, self).render(
                None, accepted_media_type, renderer_context
            )

        from rest_framework_json_api.views import RelationshipView

        if isinstance(view, RelationshipView):
            return self.render_relationship_view(
                data, accepted_media_type, renderer_context
            )

        # If `resource_name` is set to None then render default as the dev
        # wants to build the output format manually.
        if resource_name is None or resource_name is False:
            return super(JSONRenderer, self).render(
                data, accepted_media_type, renderer_context
            )

        json_api_data = data
        # initialize json_api_meta with pagination meta or an empty dict
        json_api_meta = data.get("meta", {}) if isinstance(data, dict) else {}
        included_cache = defaultdict(dict)

        if data and "results" in data:
            serializer_data = data["results"]
        else:
            serializer_data = data

        serializer = getattr(serializer_data, "serializer", None)

        included_resources = utils.get_included_resources(request, serializer)

        if serializer is not None:

            # Extract root meta for any type of serializer
            json_api_meta.update(self.extract_root_meta(serializer, serializer_data))

            if getattr(serializer, "many", False):
                json_api_data = list()

                for position in range(len(serializer_data)):
                    resource = serializer_data[position]  # Get current resource
                    resource_instance = serializer.instance[
                        position
                    ]  # Get current instance

                    if isinstance(serializer.child, PolymorphicModelSerializer):
                        # Add support for polymorphic serializer kwargs
                        resource_serializer_kwargs = serializer.child.get_serializer_kwargs(
                            resource_instance
                        )
                        resource_serializer_class = serializer.child.get_polymorphic_serializer_for_instance(
                            resource_instance
                        )(
                            context=serializer.child.context,
                            **resource_serializer_kwargs
                        )
                    else:
                        resource_serializer_class = serializer.child

                    fields = utils.get_serializer_fields(resource_serializer_class)
                    force_type_resolution = getattr(
                        resource_serializer_class, "_poly_force_type_resolution", False
                    )

                    json_resource_obj = self.build_json_resource_obj(
                        fields,
                        resource,
                        resource_instance,
                        resource_name,
                        force_type_resolution,
                    )
                    meta = self.extract_meta(serializer, resource)
                    if meta:
                        json_resource_obj.update(
                            {"meta": utils.format_field_names(meta)}
                        )
                    json_api_data.append(json_resource_obj)

                    self.extract_included(
                        fields,
                        resource,
                        resource_instance,
                        included_resources,
                        included_cache,
                    )
            else:
                fields = utils.get_serializer_fields(serializer)
                force_type_resolution = getattr(
                    serializer, "_poly_force_type_resolution", False
                )

                resource_instance = serializer.instance
                json_api_data = self.build_json_resource_obj(
                    fields,
                    serializer_data,
                    resource_instance,
                    resource_name,
                    force_type_resolution,
                )

                meta = self.extract_meta(serializer, serializer_data)
                if meta:
                    json_api_data.update({"meta": utils.format_field_names(meta)})

                self.extract_included(
                    fields,
                    serializer_data,
                    resource_instance,
                    included_resources,
                    included_cache,
                )

        # Make sure we render data in a specific order
        render_data = OrderedDict()

        if isinstance(data, dict) and data.get("links"):
            render_data["links"] = data.get("links")

        # format the api root link list
        if view.__class__ and view.__class__.__name__ == "APIRoot":
            render_data["data"] = None
            render_data["links"] = json_api_data
        else:
            render_data["data"] = json_api_data

        if included_cache:
            if isinstance(json_api_data, list):
                objects = json_api_data
            else:
                objects = [json_api_data]

            for object in objects:
                obj_type = object.get("type")
                obj_id = object.get("id")
                if obj_type in included_cache and obj_id in included_cache[obj_type]:
                    del included_cache[obj_type][obj_id]
                if not included_cache[obj_type]:
                    del included_cache[obj_type]

        if included_cache:
            render_data["included"] = list()
            for included_type in sorted(included_cache.keys()):
                for included_id in sorted(included_cache[included_type].keys()):
                    render_data["included"].append(
                        included_cache[included_type][included_id]
                    )

        if json_api_meta:
            render_data["meta"] = utils.format_field_names(json_api_meta)

        return super(renderers.JSONRenderer, self).render(
            render_data, accepted_media_type, renderer_context
        )
