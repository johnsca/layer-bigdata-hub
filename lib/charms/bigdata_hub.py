from uuid import uuid4

from charms.reactive.relations import RelationBase

from charmhelpers.core.unitdata import kv


def register_service(name, data):
    """
    Register a new external service.
    """
    if 'uuid' not in data:
        data['uuid'] = str(uuid4())
    external_services = kv().get('external-services', {})
    external_services.setdefault(name, []).append(data)
    kv().set('external-services', external_services)
    kv().flush()
    return data['uuid']


def all_services():
    """
    Combines both connected and external registered services.
    """
    services = kv().get('external-services', {})
    providers = RelationBase.from_state('hub.provider')
    if providers:
        for name, datas in providers.registered_services().items():
            services.setdefault(name, []).extend(datas)
    return services


def update_clients():
    """
    Sends the combined list of connected and external registered services
    to any connected clients.
    """
    services = all_services()
    clients = RelationBase.from_state('hub.client')
    if clients:
        clients.provide_services(services)
