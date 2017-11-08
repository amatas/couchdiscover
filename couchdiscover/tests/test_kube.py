from unittest.mock import Mock, patch
from nose.tools import assert_true
from couchdiscover.kube import KubeHostname, KubeAPIClient


@patch('couchdiscover.kube.KubeAPIClient._get_api')
@patch('couchdiscover.kube.KubeAPIClient._get_api_object')
def test_container_environment_statefulset(mock_get_api_object, mock_get_api):

    statefulset_orig = "testhost"

    mock_get_api.return_value = None
    mock_get_api_object.return_value = statefulset_orig

    host = KubeHostname("testhost-0.testhost.subdomain.domain.name")
    api = KubeAPIClient(host)
    statefulset_test = api.get_statefulset()
    statefulset_test = api._get_api_object()
    assert_true( statefulset_orig == statefulset_test)

