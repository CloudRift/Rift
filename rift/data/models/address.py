class NovaAddress(object):
    __attribute_name__ = 'nova'

    def __init__(self, name=None, region=None):
        self.name = name
        self.region = region

    def as_dict(self):
        return {
            "name": self.name,
            "region": self.region
        }

    @classmethod
    def build_from_dict(cls, address_dict):
        return cls(**address_dict)


class IpAddress(object):
    __attribute_name__ = 'ip'

    def __init__(self, address=None, port=None):
        self.address = address
        self.port = port

    def as_dict(self):
        return {
            "address": self.address,
            "port": self.port
        }

    @classmethod
    def build_from_dict(cls, address_dict):
        return cls(**address_dict)


class HostnameAddress(IpAddress):
    __attribute_name__ = 'hostname'


class Address(object):
    """ Allows for the conversion between various address model types."""

    def __init__(self, address_child=None):
        self.address_child = address_child

    def as_dict(self):
        result = {}
        if self.address_child:
            child = self.address_child
            result[child.__attribute_name__] = child.as_dict()
        return result

    @classmethod
    def build_from_dict(cls, address_dict):
        supported = [NovaAddress, IpAddress, HostnameAddress]

        # We only support one address at a time (right now)
        address_type, address_val = address_dict.items()[0]

        address_child = None
        for supported_cls in supported:
            if supported_cls.__attribute_name__ == address_type:
                address_child = supported_cls.build_from_dict(address_val)
        return Address(address_child)
