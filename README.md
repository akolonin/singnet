# SingularityNET

[![Build Status](https://travis-ci.org/singnet/singnet.svg?branch=master)](https://travis-ci.org/singnet/singnet)

[![Coverage Status](https://coveralls.io/repos/github/singnet/singnet/badge.svg)](https://coveralls.io/github/singnet/singnet)

[![Documentation Status](https://readthedocs.org/projects/singnet/badge/?version=latest)](http://singnet.readthedocs.io/en/latest/?badge=latest)

SingularityNET allows multiple AI computing agents to work as a whole to
provide various services in a distributed and decentralized way.
 
For the first time, we have a financial substrate in the blockchain that
lets us align diverse AI technologies and functions into a coherent financial
and cognitive whole. The SingularityNET architecture incorporating block-chain 
smart-contracts and automatic payment will let diverse AIs integrate together
into a single dynamic intelligence. AI agents incorporating the OpenCog AGI
framework, Google Tensorflow and other powerful tools, interacting within the
SingularityNET; will bootstrap the research and development of an AGI economy.


## Contents ##

* [**Architectural Overview**](#architectural-overview) - the system architecture
 and high-level design
* [**Example Scenario**](#example-scenario) - a non-trivial example of
 SingularityNET agent interaction
* [**SingularityNET API**](#singularitynet-api) - the interfaces required to
 implement or call agents to perform services
* [**Getting Started**](#getting-started) - instructions for getting
 SingularityNET running on your system


## Architectural Overview ##

There are seven major interacting components in the SingularityNET architecture:

* **Network** - the block-chain and smart-contract network used for agent 
  negotiation and discovery
  
* **Agent** - the agent which provides services and responds to service
 requests by other agents in the SingularityNET

* **Ontology** - contains definitions of services available in SingularityNET. 
 Ontologies are versioned and define the semantics of network operations.

* **ServiceDescriptor** - a signed immutable post-negotiation description of a
 service which can be performed by an Agent
 
* **JobDescriptor** - a list of jobs which tie a particular ServiceDescriptor with 
 job-specific data like input and output data types, URLs, specific communication
 protocols etc.

* **ServiceAdapter** - a wrapper for AI and other services which an Agent can
 invoke to perform the actual services required to perform a job according to
 the negotiated ServiceDescriptor.

* **ExternalServiceAdapter** - a wrapper for interacting with external service
 agents in the SingularityNET universe.


## Example Scenario ##
A SingularityNET Agent provides document summarization services for corporate work
groups. As inputs for this service, it might require:

* **Glossary** - a glossary of terms and entities relevant to the corporate service client

* **People Images** - a set of images representing people to be recognized

* **Object Images** - a set of images representing things to be identified
  
* **Documents** - a set of documents to summarize in accepted formats

The task of performing document summarization requires summarizing text; identifying
relevant objects and people in images; ranking relevance; processing video to
extract objects, people and a textual description; and generating
a ranked summary of the document.


### Internal Services ###

The SingularityNET Agent might perform the following services internally:

* **Final Document Summary** - assembling the parts and generating the final product

* **Text Summary** - processing the text to build a summary of text-only portions


### External Services ###

The Agent might use ExternalServiceProvider agents to perform the following services:

* **Word Sense Disambiguation** - a sub-service used by the Agent's Text Summary
 service to disambiguate words and meanings from text and context when more than
 one sense is possible and grammatically correct. 

* **Entity Extraction** - a sub-service which extracts object identities from
 images and text which match the Glossary and Images entries.

* **Video Summary** - a sub-service which extracts object identities from
 images and text which match the Glossary and both Images inputs.

* **Face Recognizer** - a sub-service which identifies people from the People
Images inputs

The architecture supports scenarios like the above where individual agents may 
provide subsets or all of the services required to deliver any Service in the
ontology.


## SingularityNET API ##


### NetworkABC ###
The base class for block-chain networks. NetworkABC defines the protocol for
managing the interactions of Agents, Ontology, ServiceDescriptors, as well as 
Agent discovery, and negotiation. Each block-chain implementation will require a
separate NetworkABC subclass which implements the smart-contracts and communication
protocols required to implement the Network ABC API.

NetworkABC subclasses must implement:
* **`join_network`** - creates a new agent on the block chain
* **`leave_network`** - removes agent from the block chain
* **`logon_network`** - opens a connection for an agent
* **`logoff_network`** - closes the connection for an agent
* **`get_network_status`** - get the agents status on the network
* **`update_ontology`** - queries the block-chain and updates the ontology to current version
* **`advertise_service`** - registers an agent's service offerings on the blockchain
* **`remove_service_advertisement`** - removes an agents service offerings from the blockchain
* **`find_service_providers`** - returns a list of external service provider agents


### ServiceAdapterABC ###
This is the base class for all Service Adapters. Services can be AI services or
other services of use by the network like file storage, backup, etc.

ServiceAdapterABC subclasses must implement:
* **`perform`** - perform the service defined by the JobDescriptor

Additionally, ServiceAdapterABC subclasses may also implement:
* **`init`** - perform service one-time initialization
* **`start`** - connect with external network providers required to perform service
* **`stop`** - disconnect in preparation for taking the service offline
* **`can_perform`** - override to implement service specific logic
* **`all_required_agents_can_perform`** - check if dependent agents can perform
 sub-services


## Getting Started ##

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. See deployment for notes on how to
deploy the project on a live system.

The agent is service responsible for communicating with the workers and the rest
of the network. You can run an agent connected to the network as a client or as
a client with underlying workers.


### Prerequisites ###

At this time, the only OS that this has been tested on is Ubuntu 16.04 LTS. This
may change in the future but for now, you must start there. There are only a
few system level requirements.

Docker and Docker Compose are used heavily. You must have a recent version of
Docker installed.

The current demo uses a 3-node setup, Alice, Bob and Charlie.

The following command will create and run the Alice node.

```
./tools.sh alice
```

In a separate terminal, you can run the Bob agent.

```
./tools.sh bob
```

In yet another separate terminal, you can run the Charlie agent.

```
./tools.sh charlie
```


### Installing ###

The install process can take a bit of time. If you run into any issue, please
do not hesitate to file a bug report. Be sure to include the last few lines of
the console output to help us determine where it failed.

You will not need sudo for the install as long as the items in the prerequisites
section have been installed properly.

<!--- this command is removed from tools.sh
```
./tools.sh prep
```
You can re-run prep over and over again as it, in most cases, will not
re-install because it does checks to make sure the component exists or not,
if it exists it does not run again.
-->

### Running the tests ###

Tests are handled by PyTest via Tox

```
./tools.sh agent-test
```


### Generating docs ###

Docs are not currently included in the source as they are changing rapidly. We
do suggest you create the docs and look them over. Once this settles, we will
likely have an online reference to these.

```
./tools.sh agent-docs
```

<!--- this is already done
## Deployment

We are working on Docker images for easy deployment. For the moment, the
installation relies on building from source on the target machine.
-->

### Quick Start ###

* Make sure you can install [https://www.docker.com/](Docker) on your target OS.
* Install Docker. For Ubuntu 16.04, here are the instructions
  Be sure to install docker as user in sudo group, not as root. If installed as root, must have to add user to docker user group. Everything is discussed in the following links.
  [Installing Docker on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
  [Installing Docker-Compose on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04)
* Checkout SingularityNET code
```
  git clone https://github.com/singnet/singnet.git
```
* Check SingularityNET installation (in root singnet folder)
```
  ./tools.sh agent-test
  ./tools.sh alice
```
* Try [other commands](https://github.com/singnet/singnet/blob/master/tools.sh)

### Trouble Shooting ###

Sometimes, is docker process is hanged blocking the port and you can not restart, shutdown the entire SingularityNET docker image with the following command:
```
$docker-compose down
```

To keep your SingulariytNET docker output to session console persistent, use Linux [screen command](https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/#starting)

## Built With

* [AIOHttp](https://aiohttp.readthedocs.io/en/stable/) - The async web
framework used to handle JSONRPC and HTML requests
* [SQLAlchemy](https://www.sqlalchemy.org/) - Internal data storage


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/opencog/singnet/tags). 

See also the list of [contributors](https://github.com/opencog/singnet/graphs/contributors) who participated in this project.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
