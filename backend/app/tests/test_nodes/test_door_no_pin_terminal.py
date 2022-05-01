import json
from tests.requests.requests import NodeRequest
from tests.requests.nodeActions import RequestUserAccess


def test_request_valid_user_access(base_setup):
    app, app_context, db, client = base_setup
    # make login request
    fingerprint = "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1"
    authentification = "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
    request = NodeRequest(fingerprint, authentification, [RequestUserAccess("112.123.23.1.91")]).to_json()
    request = client.post('http://127.0.0.1:5000/api/v1/nodes', json=json.loads(request))
    assert request.status_code == 200
    resp = json.loads(request.get_data())
    deny_action = next((item for item in resp['actions'] if item["action"] == "grandAccess"), None)
    assert deny_action is not None
    print(resp)


def test_request_invalid_user_access(base_setup):
    app, app_context, db, client = base_setup
    # make login request
    fingerprint = "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1"
    authentification = "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
    request = NodeRequest(fingerprint, authentification, [RequestUserAccess("0.0.0.0.0")]).to_json()
    request = client.post('http://127.0.0.1:5000/api/v1/nodes', json=json.loads(request))
    assert request.status_code == 200
    resp = json.loads(request.get_data())
    deny_action = next((item for item in resp['actions'] if item["action"] == "denyAccess"), None)
    assert deny_action is not None
    print(resp)
