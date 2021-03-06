import json
import logging
import os
import subprocess

from tendrl.commons.etcdobj import EtcdObj

from tendrl.ceph_integration import objects

LOG = logging.getLogger(__name__)


class TendrlContext(objects.CephIntegrationBaseObject):
    def __init__(self, integration_id=None, fsid=None, *args, **kwargs):
        super(TendrlContext, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/TendrlContext'

        # integration_id is the Tendrl generated cluster UUID
        self.integration_id = integration_id or self._get_local_integration_id()
        self.fsid = fsid or self._get_local_fsid()
        self.sds_name, self.sds_version = self._get_sds_details()
        self._etcd_cls = _TendrlContextEtcd

    def create_local_integration_id(self):
        tendrl_context_path = "/etc/tendrl/ceph-integration/integration_id"
        with open(tendrl_context_path, 'wb+') as f:
            f.write(self.integration_id)
            LOG.info("SET_LOCAL: "
                     "tendrl_ns.ceph_integration.objects.TendrlContext.integration_id"
                     "==%s" %
                     self.integration_id)

    def _get_local_integration_id(self):
        try:
            tendrl_context_path = "/etc/tendrl/ceph-integration/integration_id"
            if os.path.isfile(tendrl_context_path):
                with open(tendrl_context_path) as f:
                    integration_id = f.read()
                    if integration_id:
                        LOG.info(
                            "GET_LOCAL: "
                            "tendrl_ns.ceph_integration.objects.TendrlContext"
                            ".integration_id==%s" % integration_id)
                        return integration_id
        except AttributeError:
            return None

    def create_local_fsid(self):
        tendrl_context_path = "/etc/tendrl/ceph-integration/fsid"
        with open(tendrl_context_path, 'wb+') as f:
            f.write(self.fsid)
            LOG.info("SET_LOCAL: "
                     "tendrl_ns.ceph_integration.objects.TendrlContext.fsid"
                     "==%s" %
                     self.fsid)

    def _get_local_fsid(self):
        try:
            tendrl_context_path = "/etc/tendrl/ceph-integration/fsid"
            if os.path.isfile(tendrl_context_path):
                with open(tendrl_context_path) as f:
                    fsid = f.read()
                    if fsid:
                        LOG.info(
                            "GET_LOCAL: "
                            "tendrl_ns.ceph_integration.objects.TendrlContext"
                            ".fsid==%s" % fsid)
                        return fsid
        except AttributeError:
            return None

    def _get_sds_details(self):
        cmd = subprocess.Popen(
            "ceph version -f json",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = cmd.communicate()
        if err and 'command not found' in err:
            LOG.info("ceph not installed on host")
            return None

        if out:
            details = json.loads(out)

            version = details['version'].split()[2]
            name = details['version'].split()[0]
            return name, version



class _TendrlContextEtcd(EtcdObj):
    """A table of the tendrl context, lazily updated
    """
    __name__ = 'clusters/%s/TendrlContext'
    _tendrl_cls = TendrlContext

    def render(self):
        self.__name__ = self.__name__ % tendrl_ns.tendrl_context.integration_id
        return super(_TendrlContextEtcd, self).render()
