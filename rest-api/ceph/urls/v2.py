
from django.conf.urls import patterns, url, include
from rest_framework import routers
import ceph.views.v1
import ceph.views.v2

router = routers.DefaultRouter(trailing_slash=False)

# Presentation of django.contrib.auth.models.User
router.register(r'user', ceph.views.v1.UserViewSet)

# Information about each Ceph cluster (FSID), see sub-URLs
router.register(r'cluster', ceph.views.v2.ClusterViewSet, base_name='cluster')

# Server authentication keys, whether accepted or not
router.register(r'key', ceph.views.v2.SaltKeyViewSet, base_name='key')

# Information about authenticated servers
router.register(r'server', ceph.views.v2.ServerViewSet, base_name='server')


urlpatterns = patterns(
    '',

    # About the host calamari server is running on
    url(r'^grains', ceph.views.v2.grains),
    url(r'^info', ceph.views.v1.Info.as_view()),

    # Wrapping django auth
    url(r'^user/me', ceph.views.v1.UserMe.as_view()),
    url(r'^auth/login', ceph.views.v1.login),
    url(r'^auth/logout', ceph.views.v1.logout),

    # This has to come after /user/me to make sure that special case is handled
    url(r'^', include(router.urls)),

    # FIXME: the OSD stuff based on derived objects is a bit shonky, we are
    # currently just exposing the /v1/ style.  Needs TLC to come up with
    # nice generalised filtering for OSDs and PGs.
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/osd$', ceph.views.v1.OSDList.as_view(), name='cluster-osd-list'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/osd/(?P<osd_id>\d+)$', ceph.views.v1.OSDDetail.as_view(),
        name='cluster-osd-detail'),
    # TODO a sanitized OSD serializer similar to what we do for pools
    # TODO implement PATCH to /osd/<id> for attribute changes
    # TODO implement POST to /osd/<id>/commands/<command> for operations
    # that don't directly change an attribute, e.g. initiating scrub, repair
    # TODO expose weight information OSDs along with ability to reweight

    # About ongoing operations in cthulhu
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/request/(?P<request_id>[a-zA-Z0-9-]+)$',
        ceph.views.v2.RequestViewSet.as_view({'get': 'retrieve'}), name='cluster-request-detail'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/request$',
        ceph.views.v2.RequestViewSet.as_view({'get': 'list'}), name='cluster-request-list'),

    # OSDs, Pools, CRUSH
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/crush_rule_set$', ceph.views.v2.CrushRuleSetViewSet.as_view({'get': 'list'}),
        name='cluster-crush_rule_set-list'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/crush_rule$', ceph.views.v2.CrushRuleViewSet.as_view({'get': 'list'}),
        name='cluster-crush_rule-list'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/pool$', ceph.views.v2.PoolViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='cluster-pool-list'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/pool/(?P<pool_id>\d+)$', ceph.views.v2.PoolViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'}),
        name='cluster-pool-detail'),

    # Direct access to SyncObjects, DerivedObjects, graphite stats
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/sync_object$',
        ceph.views.v2.SyncObject.as_view({'get': 'describe'}), name='cluster-sync-object-describe'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/sync_object/(?P<sync_type>[a-zA-Z0-9-_]+)$',
        ceph.views.v2.SyncObject.as_view({'get': 'retrieve'}), name='cluster-sync-object'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/derived_object/(?P<derived_type>[a-zA-Z0-9-_]+)$',
        ceph.views.v2.DerivedObject.as_view({'get': 'retrieve'}), name='cluster-derived-object'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/derived_object$',
        ceph.views.v2.DerivedObject.as_view({'get': 'describe'}), name='cluster-derived-object-describe'),

    # All about servers
    url(r'^server/(?P<fqdn>[a-zA-Z0-9-\.]+)/grains$', ceph.views.v2.ServerViewSet.as_view({'get': 'retrieve_grains'})),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/server$', ceph.views.v2.ServerClusterViewSet.as_view({'get': 'list'}),
        name='cluster-server-list'),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/server/(?P<fqdn>[a-zA-Z0-9-\.]+)$',
        ceph.views.v2.ServerClusterViewSet.as_view({'get': 'retrieve'}), name='cluster-server-detail'),

    # Events
    url(r'^event$', ceph.views.v2.EventViewSet.as_view({'get': 'list'})),
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/event$', ceph.views.v2.EventViewSet.as_view({'get': 'list_cluster'})),
    url(r'^server/(?P<fqdn>[a-zA-Z0-9-\.]+)/event$', ceph.views.v2.EventViewSet.as_view({'get': 'list_server'})),

    # Log tail
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/log', ceph.views.v2.LogTailViewSet.as_view({'get': 'get_cluster_log'})),

    # Placement groups
    url(r'^cluster/(?P<fsid>[a-zA-Z0-9-]+)/pg/(?P<pgid>\d+\.[0-9a-z]+)/query',
        ceph.views.v2.PlacementGroupViewSet.as_view({'get': 'get_query'}))

)
