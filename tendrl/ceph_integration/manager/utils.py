import os
import os.path
import subprocess
from tendrl.commons import event
from tendrl.commons.message import Message
import traceback

TENDRL_CONTEXT = "/etc/tendrl/ceph-integration/tendrl_context"
FSID = "/etc/tendrl/ceph-integration/fsid"
NODE_CONTEXT = "/etc/tendrl/node_agent/node_context"


def get_tendrl_context():
    if os.path.isfile(TENDRL_CONTEXT):
        with open(TENDRL_CONTEXT) as f:
            cluster_id = f.read()
            try:
                event.Event(Message(
                    Message.priorities.INFO,
                    Message.publishers.CEPH_INTEGRATION,
                    {"message": "TendrlContext.integration_id=%s found!" %
                     cluster_id}))
            except event.EventFailed:
                print(traceback.format_exc())
            return cluster_id
    else:
        return None


def get_node_context():
    if os.path.isfile(NODE_CONTEXT):
        with open(NODE_CONTEXT) as f:
            node_id = f.read()
            try:
                event.Event(Message(
                    Message.priorities.INFO,
                    Message.publishers.CEPH_INTEGRATION,
                    {"message": "Node_context.node_id==%s found!" %
                     node_id}))
            except event.EventFailed:
                print(traceback.format_exc())
            return node_id


def get_fsid():
    # check if valid uuid is already present in node_context
    # if not present generate one and update the file
    if os.path.isfile(FSID):
        with open(FSID) as f:
            fsid = f.read()
            if fsid:
                try:
                    event.Event(Message(
                        Message.priorities.INFO,
                        Message.publishers.CEPH_INTEGRATION,
                        {"message": "TendrlContext.fsid==%s found!" %
                         fsid}))
                except event.EventFailed:
                    print(traceback.format_exc())
                return fsid
    else:
        return None


def set_fsid(fsid):
    current_fsid = get_fsid()
    if current_fsid is None:
        with open(FSID, 'wb+') as f:
            f.write(fsid)
            current_fsid = fsid
            try:
                event.Event(Message(
                    Message.priorities.INFO,
                    Message.publishers.CEPH_INTEGRATION,
                    {"message": "TendrlContext.fsid==%s created!" %
                     fsid}))
            except event.EventFailed:
                print(traceback.format_exc())

    return current_fsid


def get_sds_version():
    res = subprocess.check_output(['ceph', '--version'])
    return res.split()[2].split("-")[0]
