from hdmf.common import ExternalResources
from pynwb import get_type_map, register_class
from hdmf.utils import docval, get_docval, call_docval_func


@register_class('NWBExternalResources', 'ndx-external-resources')
class NWBExternalResources(ExternalResources):

    @docval(*get_docval(ExternalResources.__init__))
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)
        self.type_map = kwargs['type_map'] or get_type_map()
