# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension for storing external resource references""",
        name="""ndx-external-resources""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_namespace('core')
    ns_builder.include_type('ExternalResources', namespace='hdmf-experimental')  # TODO migrate to core

    er_nwbfile_spec = NWBGroupSpec(
        neurodata_type_def='ERNWBFile',
        neurodata_type_inc='NWBFile',
        doc=('Extension of the NWBFile class to allow placing the new external resources group. '
             'NOTE: If this proposal for extension to NWB gets merged with the core schema, then this type would be '
             'removed and the NWBFile specification updated instead.'),
        groups=[
            NWBGroupSpec(
                name='.external_resources',
                neurodata_type_inc='NWBExternalResources',
                doc='External resources used in this file.',
            ),
        ],
    )

    nwb_er_spec = NWBGroupSpec(
        neurodata_type_def='NWBExternalResources',
        neurodata_type_inc='ExternalResources',
        doc='A set of four tables for tracking external resource references in a file.',
    )

    new_data_types = [er_nwbfile_spec, nwb_er_spec]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
