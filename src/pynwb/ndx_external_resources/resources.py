from hdmf.common import ExternalResources as hdmf_ExternalResources
from pynwb import get_type_map
from hdmf.utils import docval, get_docval, call_docval_func


class ExternalResources(hdmf_ExternalResources):

    @docval(*get_docval(hdmf_ExternalResources.__init__))
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)
        self.type_map = kwargs['type_map'] or get_type_map()
