from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.manager import utils as manager_utils
from tendrl.ceph_integration import objects


class Create(objects.CephIntegrationBaseAtom):
    def __init__(self, config=None, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)
        self.obj = objects.Pool

    def run(self, parameters):
        fsid = manager_utils.get_fsid()
        attrs = dict(name=parameters['Pool.poolname'],
                     pg_num=parameters['Pool.pg_num'],
                     min_size=parameters['Pool.min_size'])
        crud = Crud(parameters['manager'])
        crud.create(fsid, "pool", attrs)
        return True
