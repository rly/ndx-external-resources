# TODO move these functions to PyNWB core

import datetime

from hdmf.build import TypeMap
from pynwb import TimeSeries, NWBHDF5IO
from pynwb.core import DynamicTable
from pynwb.testing import TestCase, remove_test_file

from ndx_external_resources import ERNWBFile, NWBExternalResources

def set_up_nwbfile():
    nwbfile = ERNWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    return nwbfile

class TestERNWBFile(TestCase):

    def test_constructor_basic(self):
        """Test that the constructor for ERNWBFile creates an empty ExternalResources."""
        nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.assertIsInstance(nwbfile.external_resources, NWBExternalResources)
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
                         (table['test_col'].object_id, '', ''))


class TestExternalResources(TestCase):

    def test_type_map(self):
        er = NWBExternalResources('ER')
        self.assertEqual(er.type_map.namespace_catalog.namespaces,
                         ('hdmf-common', 'hdmf-experimental', 'core', 'ndx-external-resources'))

    def test_custom_type_map(self):
        type_map = TypeMap()
        er = NWBExternalResources('ER', type_map=type_map)
        self.assertIs(er.type_map, type_map)


class TestTaskSeriesRoundtrip(TestCase):
    """Simple roundtrip test for ER."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
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
            field='unit',
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

        with NWBHDF5IO(path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertEqual(len(read_nwbfile.external_resources.objects), 2)
            self.assertEqual(len(read_nwbfile.external_resources.object_keys), 2)
            self.assertEqual(len(read_nwbfile.external_resources.keys), 2)
            self.assertEqual(len(read_nwbfile.external_resources.resources), 2)
            self.assertEqual(len(read_nwbfile.external_resources.entities), 2)

            self.assertEqual(list(read_nwbfile.external_resources.objects[0]),
                             list(nwbfile.external_resources.objects[0]))
            self.assertEqual(list(read_nwbfile.external_resources.objects[1]),
                             list(nwbfile.external_resources.objects[1]))
