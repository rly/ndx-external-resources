from pynwb import register_class
from pynwb.file import NWBFile
from hdmf.utils import docval, get_docval, call_docval_func, popargs
from hdmf.common import ExternalResources  # TODO import this from pynwb after ExternalResources is aliased in PyNWB


@register_class('ERNWBFile', 'ndx-external-resources')
class ERNWBFile(NWBFile):

    __nwbfields__ = (
        {'name': 'external_resources', 'child': True, 'required_name': '.external_resources'},
    )

    @docval(*get_docval(NWBFile.__init__),
            {'name': 'external_resources',
             'type': 'ExternalResources',
             'doc': 'The external resources that objects in the file are related to',
             'default': None},)
    def __init__(self, **kwargs):
        external_resources = popargs('external_resources', kwargs)
        call_docval_func(super().__init__, kwargs)
        if external_resources is not None:
            self.external_resources = external_resources
        else:
            self.external_resources = ExternalResources('.external_resources')
