# TODO move these functions to PyNWB core

import datetime

from hdmf.common import ExternalResources
from pynwb import TimeSeries
from pynwb.core import DynamicTable
from pynwb.testing import TestCase

from ndx_external_resources import ERNWBFile


class TestERNWBFile(TestCase):

    def test_constructor_basic(self):
        """Test that the constructor for ERNWBFile creates an empty ExternalResources."""
        nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.assertIsInstance(nwbfile.external_resources, ExternalResources)
        self.assertEqual(nwbfile.external_resources.name, '.external_resources')
        self.assertEqual(len(nwbfile.external_resources.objects), 0)
        self.assertEqual(len(nwbfile.external_resources.object_keys), 0)
        self.assertEqual(len(nwbfile.external_resources.keys), 0)
        self.assertEqual(len(nwbfile.external_resources.resources), 0)
        self.assertEqual(len(nwbfile.external_resources.entities), 0)

    def test_add_ref(self):
        """Test that ExternalResources.add_ref works with containers in the ERNWBFile."""
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

        self.assertEqual(len(nwbfile.external_resources.objects), 2)
        self.assertEqual(len(nwbfile.external_resources.object_keys), 2)
        self.assertEqual(len(nwbfile.external_resources.keys), 2)
        self.assertEqual(len(nwbfile.external_resources.resources), 2)
        self.assertEqual(len(nwbfile.external_resources.entities), 2)

        self.assertEqual(nwbfile.external_resources.objects[0],
                         (container.object_id, 'TimeSeries/data/unit', ''))
        self.assertEqual(nwbfile.external_resources.objects[1],
                         (table.columns[0].object_id, '', ''))

    def test_type_map(self):
        nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        _type_map = nwbfile.external_resources.type_map
        self.assertEqual(_type_map.namespace_catalog.namespaces, ('hdmf-common', 'hdmf-experimental', 'core', 'ndx-external-resources'))
