import json
from tests.requests.requests import NodeRequest
from tests.requests.nodeActions import RegisterNodeStartup


def test_register_node_startup(base_setup):
    app, app_context, db, client = base_setup
    # make login request
    fingerprint = "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1"
    authentification = "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
    request = NodeRequest(fingerprint, authentification, [RegisterNodeStartup()]).to_json()
    login_request = client.post('http://127.0.0.1:5000/api/v1/nodes', json=json.loads(request))
    assert login_request.status_code == 200
