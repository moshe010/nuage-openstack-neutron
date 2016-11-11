# Copyright 2014 Alcatel-Lucent USA Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron.api import extensions
from neutron_lib.api import validators
from neutron_lib import exceptions


class RtrItfAddIncompleteRouterOnVsd(exceptions.BadRequest):
    message = _("Router %(id)s does not hold default zone OR domain in VSD. "
                "Router-IF add failed")


class RtrItfAddVsdSubnetNotFound(exceptions.BadRequest):
    message = _("Subnet %(subnet)s does not hold Nuage VSD reference. "
                "Router-IF add failed")


class RtrItfAddSubnetIsVsdManaged(exceptions.BadRequest):
    message = _("Subnet %(subnet)s is a VSD-Managed subnet. "
                "Router-IF add failed")


class RtrItfAddDifferentNetpartitions(exceptions.BadRequest):
    message = _("Subnet %(subnet)s and Router %(router)s belong to different "
                "net_partition Router-IF add not permitted")


class RtrItfAddSubnetHasVMs(exceptions.BadRequest):
    message = _("Subnet %(subnet)s has one or more active VMs Router-IF add "
                "not permitted")


class RtrItfAddSubnetHasVports(exceptions.BadRequest):
    message = _("Subnet %(subnet)s has one or more nuage VPORTS Router-IF add "
                "not permitted")


class RtrItfAddSubnetHasRedirectTargets(exceptions.BadRequest):
    message = _("Subnet %(subnet)s has one or more nuage redirect targets "
                "Router-IF add not permitted")


def _ecmp_count_info():
    return _("ecmp count must be a number between 1 and 8 (inclusive)")


def ecmp_count_validation(data, valid_values=None):
    if data is None:
        return

    if isinstance(data, bool):
        return _ecmp_count_info()

    try:
        data = int(data)
    except (ValueError, TypeError):
        return _ecmp_count_info()

    if data < 1 or data > 8:
        return _ecmp_count_info()


def convert_to_uppercase(data):
    if data:
        return str(data).upper()


validators.add_validator('type:ecmp_count', ecmp_count_validation)

EXTENDED_ATTRIBUTES_2_0 = {
    'routers': {
        'net_partition': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None}
        },
        'rd': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None},
            'enforce_policy': True
        },
        'rt': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None},
            'enforce_policy': True
        },
        'nuage_backhaul_vnid': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None},
            'enforce_policy': True
        },
        'nuage_backhaul_rd': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None},
            'enforce_policy': True
        },
        'nuage_backhaul_rt': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:string_or_none': None},
            'enforce_policy': True
        },
        'nuage_router_template': {
            'allow_post': True,
            'allow_put': False,
            'is_visible': True,
            'default': None,
            'validate': {'type:uuid_or_none': None}
        },
        'tunnel_type': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': 'DEFAULT',
            'validate': {'type:values': ['VXLAN', 'vxlan', 'GRE', 'gre',
                                         'DEFAULT', 'default']},
            'convert_to': convert_to_uppercase,
            'enforce_policy': True,
        },
        'ecmp_count': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:ecmp_count': None},
            'enforce_policy': True
        },
    },
}


class Nuage_router(extensions.ExtensionDescriptor):
    """Extension class supporting nuage router."""

    @classmethod
    def get_name(cls):
        return "Nuage router"

    @classmethod
    def get_alias(cls):
        return "nuage-router"

    @classmethod
    def get_description(cls):
        return "Nuage Router"

    @classmethod
    def get_namespace(cls):
        return "http://nuagenetworks.net/ext/routers/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2014-01-01T10:00:00-00:00"

    def get_extended_resources(self, version):
        if version == "2.0":
            return EXTENDED_ATTRIBUTES_2_0
        else:
            return {}
