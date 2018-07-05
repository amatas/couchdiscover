from unittest.mock import Mock, patch
from nose.tools import assert_true
from couchdiscover.kube import KubeHostname
from couchdiscover.couch import CouchServer, CouchInitClient, CouchManager
import json


class Environment:
    host = KubeHostname("testhost-3.testhost.subdomain.domain.name")
    ports = ('5984', '5986')
    creds = ('adm', 'pass')

env = Environment()

@patch('couchdiscover.couch.CouchInitClient.__init__')
@patch('couchdiscover.couch.CouchInitClient.cluster_nodes')
def test_CouchManager_node_in_cluster(mock_cluster_nodes, mock_init):

    mock_init.return_value = None
    mock_cluster_nodes.return_value = [
        "couchdb@testhost-0.testhost.subdomain.domain.local",
        "couchdb@testhost-1.testhost.subdomain.domain.local",
        "couchdb@testhost-2.testhost.subdomain.domain.local"
        ]
    node = "couchdb@testhost-0.testhost.subdomain.domain.local"
    manager = CouchManager(env)
    assert_true( hasattr(manager, 'node_in_cluster') )
    assert_true( manager.node_in_cluster( node ) )


@patch('couchdiscover.couch.CouchInitClient.__init__')
@patch('couchdiscover.couch.CouchInitClient._wait_for_couch')
@patch('couchdiscover.couch.CouchInitClient.membership')
def test_CouchInitClient_cluster_nodes(mock_membership, mock_wait, mock_init):
    data = """
{
  "all_nodes":
  [
    "couchdb@testhost-0.testhost.subdomain.domain.local",
    "couchdb@testhost-1.testhost.subdomain.domain.local",
    "couchdb@testhost-2.testhost.subdomain.domain.local"
  ],
  "cluster_nodes":
  [
    "couchdb@testhost-0.testhost.subdomain.domain.local",
    "couchdb@testhost-1.testhost.subdomain.domain.local",
    "couchdb@testhost-2.testhost.subdomain.domain.local"
  ]
}
"""

    hostname = "couchdb@testhost-0.testhost.subdomain.domain.local"
    mock_membership.return_value = json.loads(data)
    mock_wait.return_value = None
    mock_init.return_value = None
    client = CouchInitClient()
    assert_true( hasattr(client, 'cluster_nodes') )
    assert_true( isinstance(client.cluster_nodes(), list  ))
    assert_true( hostname in client.cluster_nodes() )

@patch('couchdiscover.couch.CouchInitClient.__init__')
@patch('couchdiscover.couch.CouchInitClient.cluster_nodes')
def test_CouchManager_balance_shards(mock_cluster_nodes, mock_init):

    mock_init.return_value = None
    mock_cluster_nodes.return_value = [
        "couchdb@testhost-0.testhost.subdomain.domain.local",
        "couchdb@testhost-1.testhost.subdomain.domain.local",
        "couchdb@testhost-2.testhost.subdomain.domain.local"
        ]

    node = "couchdb@testhost-2.testhost.subdomain.domain.local"
    manager = CouchManager(env)
    assert_true( hasattr(manager, 'balance_shards') )


@patch('couchdiscover.couch.CouchServer.__init__')
def test_CouchServer_all_dbs(mock_init):

    mock_init.return_value = None
    server = CouchServer(env)
    assert_true( hasattr(server, 'all_dbs') )

@patch('couchdiscover.couch.CouchServer.__init__')
def test_CouchServer_get_shard_config(mock_init):

    mock_init.return_value = None
    server = CouchServer(env)
    assert_true( hasattr(server, 'get_shard_config') )

@patch('couchdiscover.couch.CouchServer.__init__')
def test_CouchServer_save_shard_config(mock_init):

    mock_init.return_value = None
    server = CouchServer(env)
    assert_true( hasattr(server, 'save_shard_config') )

@patch('couchdiscover.couch.CouchManager.__init__')
def test_CouchManager_fix_shard_config(mock_init):

    mock_init.return_value = None
    nodes  = [
        "couchdb@testhost-0.testhost.subdomain.domain.local",
        "couchdb@testhost-1.testhost.subdomain.domain.local",
        "couchdb@testhost-2.testhost.subdomain.domain.local"
        ]
    dbs = [
        "_sysdb",
        "testdb"
        ]
    manager = CouchManager(env)

    out_shard = """
{
  "_id": "testdb",
  "_rev": "5-b4eacf2f9644f2ec71b9234726a73898",
  "shard_suffix": [
    46,
    49,
    53,
    48,
    57,
    56,
    49,
    49,
    56,
    48,
    51
  ],
  "changelog": [
    [
      "add",
      "00000000-1fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "00000000-1fffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "00000000-1fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "20000000-3fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "20000000-3fffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "20000000-3fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "40000000-5fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "40000000-5fffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "40000000-5fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "60000000-7fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "60000000-7fffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "60000000-7fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "80000000-9fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "80000000-9fffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "80000000-9fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "a0000000-bfffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "a0000000-bfffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "a0000000-bfffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "c0000000-dfffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "c0000000-dfffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "c0000000-dfffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "e0000000-ffffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "e0000000-ffffffff",
      "couchdb@testhost-1.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "e0000000-ffffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ]
  ],
  "by_node": {
    "couchdb@testhost-0.testhost.subdomain.domain.local": [
      "00000000-1fffffff",
      "20000000-3fffffff",
      "40000000-5fffffff",
      "60000000-7fffffff",
      "80000000-9fffffff",
      "a0000000-bfffffff",
      "c0000000-dfffffff",
      "e0000000-ffffffff"
    ],
    "couchdb@testhost-1.testhost.subdomain.domain.local": [
      "00000000-1fffffff",
      "20000000-3fffffff",
      "40000000-5fffffff",
      "60000000-7fffffff",
      "80000000-9fffffff",
      "a0000000-bfffffff",
      "c0000000-dfffffff",
      "e0000000-ffffffff"
    ],
    "couchdb@testhost-2.testhost.subdomain.domain.local": [
      "00000000-1fffffff",
      "20000000-3fffffff",
      "40000000-5fffffff",
      "60000000-7fffffff",
      "80000000-9fffffff",
      "a0000000-bfffffff",
      "c0000000-dfffffff",
      "e0000000-ffffffff"
    ]
  },
  "by_range": {
    "00000000-1fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "20000000-3fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "40000000-5fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "60000000-7fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "80000000-9fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "a0000000-bfffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "c0000000-dfffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "e0000000-ffffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-1.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ]
  }
}

"""

    in_shard = """
{
  "_id": "testdb",
  "_rev": "5-b4eacf2f9644f2ec71b9234726a73898",
  "shard_suffix": [
    46,
    49,
    53,
    48,
    57,
    56,
    49,
    49,
    56,
    48,
    51
  ],
  "changelog": [
    [
      "add",
      "00000000-1fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "00000000-1fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "20000000-3fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "20000000-3fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "40000000-5fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "40000000-5fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "60000000-7fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "60000000-7fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "80000000-9fffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "80000000-9fffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "a0000000-bfffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "a0000000-bfffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "c0000000-dfffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "c0000000-dfffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "e0000000-ffffffff",
      "couchdb@testhost-0.testhost.subdomain.domain.local"
    ],
    [
      "add",
      "e0000000-ffffffff",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ]
  ],
  "by_node": {
    "couchdb@testhost-0.testhost.subdomain.domain.local": [
      "00000000-1fffffff",
      "20000000-3fffffff",
      "40000000-5fffffff",
      "60000000-7fffffff",
      "80000000-9fffffff",
      "a0000000-bfffffff",
      "c0000000-dfffffff",
      "e0000000-ffffffff"
    ],
    "couchdb@testhost-2.testhost.subdomain.domain.local": [
      "00000000-1fffffff",
      "20000000-3fffffff",
      "40000000-5fffffff",
      "60000000-7fffffff",
      "80000000-9fffffff",
      "a0000000-bfffffff",
      "c0000000-dfffffff",
      "e0000000-ffffffff"
    ]
  },
  "by_range": {
    "00000000-1fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "20000000-3fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "40000000-5fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "60000000-7fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "80000000-9fffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "a0000000-bfffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "c0000000-dfffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ],
    "e0000000-ffffffff": [
      "couchdb@testhost-0.testhost.subdomain.domain.local",
      "couchdb@testhost-2.testhost.subdomain.domain.local"
    ]
  }
}
"""

    assert_true( hasattr(manager, 'fix_shard_config') )
    assert_true( isinstance(manager.fix_shard_config(nodes=nodes), str ))
    assert_true( isinstance(manager.fix_shard_config(shard_config=in_shard), str ))
    assert_true( json.dumps(json.loads(out_shard)) == manager.fix_shard_config(nodes=nodes, shard_config=json.loads(in_shard)))

