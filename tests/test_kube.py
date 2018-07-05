import unittest
from nose.tools import assert_true, assert_false
from couchdiscover import KubeHostname

class TestKube(unittest.TestCase):

    def testStatefulsetMaster(self):
        k = KubeHostname("couchdb-0.couchdb.gpii.svc.cluster.local")
        assert_true ( k.node == "couchdb-0" )
        assert_true ( k.is_master )

    def testStatefulset(self):
        k = KubeHostname("couchdb-1.couchdb.gpii.svc.cluster.local")
        assert_true ( k.node == "couchdb-1" )
        assert_false ( k.is_master )

    def testHelmStatefulsetMaster(self):
        k = KubeHostname("release-couchdb-0.couchdb.gpii.svc.cluster.local")
        assert_true ( k.node == "release-couchdb-0" )
        assert_true ( k.is_master )

    def testHelmStatefulset(self):
        k = KubeHostname("release-couchdb-1.couchdb.gpii.svc.cluster.local")
        assert_true ( k.node == "release-couchdb-1" )
        assert_false ( k.is_master )

    def testFQDNStatefulset(self):
        k = KubeHostname("release-couchdb-1.couchdb.gpii.svc.cluster.local")
        assert_true ( k.fqdn == "release-couchdb-1.couchdb.gpii.svc.cluster.local" )
