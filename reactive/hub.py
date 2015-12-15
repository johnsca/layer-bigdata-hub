from charms.reactive import when, when_not
from charmhelpers.core import hookenv
from charms.bigdata_hub import all_services


@when_not('hub.client')
def waiting():
    hookenv.status_set('active', 'Waiting for clients / providers')


@when('hub.client')
def provide_services(clients):  # pylint: disable=unused-argument
    services = all_services()
    hookenv.status_set('active', 'Providing {} services'.format(len(services)))
    clients.provide_services(services)
