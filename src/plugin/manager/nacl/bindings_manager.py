import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.nacl.bindings_connector import NACLBindingsConnector
from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class NACLBindingsManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Network ACL"
        self.cloud_service_type = "Network ACL Binding"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/nacl/bindings.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/network_acl.png"
            },
            labels=["Networking", "Security"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        bindings_connector = NACLBindingsConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = bindings_connector.get_bindings(secret_data, AVAILABLE_REGION)
            for resource in resources:
                reference = {
                    "resource_id": resource.get("id")
                }
                cloud_service = make_cloud_service(
                    name=resource['id'],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=resource,
                    account=secret_data.get("username", None),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service

