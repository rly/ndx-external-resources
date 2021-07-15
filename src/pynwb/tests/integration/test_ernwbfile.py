# TODO move these functions to PyNWB core

import datetime

from hdmf.common import ExternalResources
from pynwb import NWBHDF5IO, TimeSeries, validate as pynwb_validate
from pynwb.core import DynamicTable
from pynwb.testing import TestCase, remove_test_file

from ndx_external_resources import ERNWBFile


class TestERNWBFileRoundTrip(TestCase):

    def setUp(self):
        self.nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_empty(self):
        """Test writing and reading empty ontology_terms and ontology_objects tables."""

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertIsInstance(read_nwbfile.external_resources, ExternalResources)
            self.assertEqual(len(read_nwbfile.external_resources.objects), 0)
            self.assertEqual(len(read_nwbfile.external_resources.object_keys), 0)
            self.assertEqual(len(read_nwbfile.external_resources.keys), 0)
            self.assertEqual(len(read_nwbfile.external_resources.resources), 0)
            self.assertEqual(len(read_nwbfile.external_resources.entities), 0)

    def test_roundtrip(self):
        """Test writing and reading the ontology_terms and ontology_objects tables."""

        container = TimeSeries(
            name='test_ts',
            data=[1, 2, 3],
            unit='meters',
            timestamps=[0.1, 0.2, 0.3],
        )
        self.nwbfile.add_acquisition(container)

        table = DynamicTable(name='test_table', description='test table description')
        table.add_column(name='test_col', description='test column description')
        table.add_row(test_col='Mouse')

        self.nwbfile.add_acquisition(table)

        self.nwbfile.external_resources.add_ref(
            container=container,
            field='unit',
            key='meters',
            resource_name='SI_Ontology',
            resource_uri='',
            entity_id='5',
            entity_uri='',
        )

        self.nwbfile.external_resources.add_ref(
            container=table,
            field='test_col',
            key='Mouse',
            resource_name='NCBI_Taxonomy',
            resource_uri='https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi',
            entity_id='10090',
            entity_uri='https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=info&id=10090',
        )

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(self.nwbfile.external_resources, read_nwbfile.external_resources)
            errors = pynwb_validate(io, namespace='ndx-external-resources')
            if errors:
                for err in errors:
                    raise Exception(err)
