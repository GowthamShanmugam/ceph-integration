from tendrl.commons.etcdobj import EtcdObj
from tendrl.commons import config as cmn_config

from tendrl.ceph_integration import objects


class Config(objects.CephIntegrationBaseObject):
    def __init__(self, config=None, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        self.value = '_tendrl/config/ceph_integration'
        self.data = config or cmn_config.load_config(
            'ceph-integration',
            "/etc/tendrl/ceph-integration/ceph-integration.conf.yaml")
        self._etcd_cls = _ConfigEtcd


class _ConfigEtcd(EtcdObj):
    """Config etcd object, lazily updated
        """
    __name__ = '_tendrl/config/ceph_integration'
    _tendrl_cls = Config
