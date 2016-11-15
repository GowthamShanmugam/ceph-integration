import logging
import os
import os.path

LOG = logging.getLogger(__name__)
TENDRL_CONTEXT = "/etc/tendrl/ceph_integration/tendrl_context"
NODE_CONTEXT = "/etc/tendrl/node_agent/node_context"


def get_tendrl_context():
    # check if valid uuid is already present in tendrl_context
    # if not present generate one and update the file
    if os.path.isfile(TENDRL_CONTEXT):
        with open(TENDRL_CONTEXT) as f:
            cluster_id = f.read()
            LOG.info("Tendrl Cluster.id==%s found!" % cluster_id)
            return cluster_id


def set_tendrl_context(cluster_id):
    with open(TENDRL_CONTEXT, 'wb+') as f:
        f.write(cluster_id)
        LOG.info("Tendrl Cluster.id==%s created!" % cluster_id)


def get_node_context():
    if os.path.isfile(NODE_CONTEXT):
        with open(NODE_CONTEXT) as f:
            node_id = f.read()
            LOG.info("Tendrl Node.id==%s found!" % node_id)
            return node_id
