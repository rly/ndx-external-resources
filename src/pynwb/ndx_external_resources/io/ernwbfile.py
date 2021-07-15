from pynwb import register_map
from pynwb.io.file import NWBFileMap

from ..ernwbfile import ERNWBFile


@register_map(ERNWBFile)
class ERNWBFileMap(NWBFileMap):

    def __init__(self, spec):
        super().__init__(spec)
        self.map_spec('external_resources', self.spec.get_group('.external_resources'))
