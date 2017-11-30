# tests/test_aigents_adapters.py - unit test for the tensorflow MNIST adapter.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
from pathlib import Path

import pytest

from adapters.aigents import AigentsRSSFeederAdapter, AIGENTS_RSS_FEEDER_ID
from sn_agent import ontology as onto
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.log import setup_logging
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter import setup_service_manager
from sn_agent.test.mocks import MockApp

log = logging.getLogger(__name__)

TEST_DIRECTORY = Path(__file__).parent


@pytest.fixture
def app():
    app = MockApp()
    onto.setup_ontology(app)
    return app


def test_aigents_rss_feeder_adapter(app):
    setup_logging()
    log.debug("Testing Aigents RSS Feeder Adapter")

    type = 'rss_feed' #TODO make parameter
    data = {'area': 'test'}

    # Setup a test jobpretending to reach Aigents RSS Feeder
    job_parameters = {  'input_type': 'attached',
                        'input_data': {
                            'type' : type, 'data' : data
                        },
                        'output_type': 'attached'
                 }

    # Get the service by ID. A service identifies a unique service provided by
    # SingularityNET and is part of the ontology.
    ontology = app['ontology']
    aigents_service = ontology.get_service(AIGENTS_RSS_FEEDER_ID)

    # Create the service adapter.
    service_adapter = AigentsRSSFeederAdapter(app, aigents_service)

    # Create a service descriptor. These are post-contract negotiated descriptors that may include
    # other parameters like quality of service, input and output formats, etc.
    service_descriptor = ServiceDescriptor(AIGENTS_RSS_FEEDER_ID)

    # Create a new job descriptor for test
    job_list = [job_parameters]
    job = JobDescriptor(service_descriptor, job_list)

    # Setup the service manager. NOTE: This will add services that are (optionally) passed in
    # so you can manually create services in addition to those that are loaded from the config
    # file. After all the services are added, it will call post_load_initialize on all the
    # services.
    setup_service_manager(app, [service_adapter])

    # Test perform for the service adapter.
    try:
        exception_caught = False
        results = service_adapter.perform(job)
    except RuntimeError as exception:
        exception_caught = True
        log.error("    Exception caught %s", exception)
        log.debug("    Error performing %s %s", job, service_adapter)
    assert not exception_caught

    # Check our results for format and content.
    assert len(results) == 1
    assert results[0]['adapter_type'] == 'aigents'
    assert results[0]['response_data'] == 'Ok.'

    if results[0]['adapter_type'] == 'aigents' and results[0]['response_data'] == 'Ok.':
        log.debug("Aigents Adapter for "+type+" - Test Passed")
