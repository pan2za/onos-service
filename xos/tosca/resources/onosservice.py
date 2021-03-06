from service import XOSService
from core.models import ServiceAttribute
from services.onos.models import ONOSService

class XOSONOSService(XOSService):
    provides = "tosca.nodes.ONOSService"
    xos_model = ONOSService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "versionNumber", "rest_hostname", "rest_port", "no_container", "node_key"]

    def set_service_attr(self, obj, prop_name, value):
        value = self.try_intrinsic_function(value)
        if value:
            attrs = ServiceAttribute.objects.filter(service=obj, name=prop_name)
            if attrs:
                attr = attrs[0]
                if attr.value != value:
                    self.info("updating attribute %s" % prop_name)
                    attr.value = value
                    attr.save()
            else:
                self.info("adding attribute %s" % prop_name)
                ta = ServiceAttribute(service=obj, name=prop_name, value=value)
                ta.save()

    def postprocess(self, obj):
        props = self.nodetemplate.get_properties()
        for (k,d) in props.items():
            v = d.value
            if k.startswith("config_"):
                self.set_service_attr(obj, k, v)
            elif k.startswith("rest_")  and (k!="rest_hostname") and (k!="rest_port"):
                self.set_service_attr(obj, k, v)

