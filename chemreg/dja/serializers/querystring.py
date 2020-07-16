import re
from collections.abc import Mapping

from rest_framework import serializers


class QueryStringSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        renameval = r"([^=&]+)(?:=([^&]*))?"
        rekeys = r"(?:(?<=^).*?(?=%5B))|(?:(?<=%5B).*?(?=%5D))"
        ret = {}
        for name, val in re.findall(renameval, data):
            keys = re.findall(rekeys, name, flags=re.I) or [name]
            vals = val.split(",")
            nested = ret
            # create nested dictionaries
            for key in keys[:-1]:
                if key not in nested:
                    nested[key] = {}
                nested = nested[key]
            # set value
            # TODO: throw error on overwrite
            if len(vals) == 1:
                nested[keys[-1]] = vals[0] or True
            else:
                nested[keys[-1]] = vals
        return super().to_internal_value(ret)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        stack = list(([k], v) for k, v in data.items())
        params = []
        while stack:
            keys, val = stack.pop()
            if isinstance(val, Mapping):
                stack.extend((keys + [k], v) for k, v in data.items())
            else:
                keystr = keys.popleft()
                for key in keys:
                    keystr += f"%5B{key}%5D"
                if not val:
                    params.append(keystr)
                elif isinstance(val, list):
                    params.append(keystr + f"={','.join(val)}")
                else:
                    params.append(keystr + f"={val}")
        return "&".join(params)
