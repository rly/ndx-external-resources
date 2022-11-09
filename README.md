# ndx-external-resources Extension for NWB

## Status

This extension is intended to facilate evaluation of ExternalResources with NWB. If this proposal for extension to NWB gets merged with the core schema, then this type would be removed and the NWBFile specification updated instead. As such, this extension is not intended for production use.

## Installation


## Usage

```python
# TODO move these functions to PyNWB core

import datetime
from pynwb import TimeSeries, NWBHDF5IO
from pynwb.core import DynamicTable

from ndx_external_resources import ERNWBFile


nwbfile = ERNWBFile(
    session_description='session_description',
    identifier='identifier',
    session_start_time=datetime.datetime.now(datetime.timezone.utc)
)

container = TimeSeries(
    name='test_ts',
    data=[1, 2, 3],
    unit='meters',
    timestamps=[0.1, 0.2, 0.3],
)
nwbfile.add_acquisition(container)

table = DynamicTable(name='test_table', description='test table description')
table.add_column(name='test_col', description='test column description')
table.add_row(test_col='Mouse')

nwbfile.add_acquisition(table)

nwbfile.external_resources.add_ref(
    container=container,
    attribute='unit',
    key='meters',
    resource_name='SI_Ontology',
    resource_uri='',
    entity_id='5',
    entity_uri='',
)

nwbfile.external_resources.add_ref(
    container=table,
    attribute='test_col',
    key='Mouse',
    resource_name='NCBI_Taxonomy',
    resource_uri='https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi',
    entity_id='10090',
    entity_uri='https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=info&id=10090',
)

path = 'test.nwb'
with NWBHDF5IO(path, mode='w') as io:
    io.write(nwbfile)
io = NWBHDF5IO(path, mode='r', load_namespaces=True)
read_nwbfile = io.read()
read_container = read_nwbfile.acquisition['test_ts']
read_nwbfile.external_resources.get_object_resources(read_container, 'TimeSeries/data/unit')
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
