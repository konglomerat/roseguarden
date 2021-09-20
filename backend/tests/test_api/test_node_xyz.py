# %%

import requests

# make login request
json_data = {
    'actions': [{
        'action': 'login',
        'password': 'test',
        'username': 'test@fabba.space',
        'version': 1,
        'workspace': 'users'
    }],
    'data':
    None,
    'head': {
        'msgId': 1,
        'requestType': '',
        'session': 'bK0GIzkTfybtIjWPZGWt_x05f0HHB2_0sfcJYEshvLE',
        'source': 'webclient',
        'target': 'webserver',
        'version': '1.0'
    }
}

node_request = requests.post('https://roseguarden.fabba.space/api/v1/nodes', json=json_data)
print(node_request.status_code, node_request.reason, node_request.content)
