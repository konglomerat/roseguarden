import json


class TestAction:
    def test_login(self, base_setup):

        app, app_context, db, client = base_setup
        # make login request
        jwt = {
            'actions': [{
                'action': 'login',
                'password': 'test1234',
                'username': 'roseguarden@fabba.space',
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
        login_request = client.post('http://127.0.0.1:5000/api/v1', json=jwt)
        assert login_request.status_code == 200
        resp = json.loads(login_request.get_data())
        notify_action = next(item for item in resp['actions'] if item["action"] == "notify")
        assert notify_action['messagetype'] == 'success'
        print(resp)
        resp = login_request.response[0]
        print(resp)
        # print(login_request.status_code, login_request.reason, login_request.content)
        # print('----')
        # print(login_request.cookies)
        # print("csrf_access_token: ", login_request.cookies['csrf_access_token'])

        # extract cookies from login_request
        # cookies = requests.utils.dict_from_cookiejar(login_request.cookies)

        # action = {'username': 'test', 'password': 'test'}
        # headers = {'X-CSRF-TOKEN': login_request.cookies['csrf_access_token']}

        # print("")
        # print("make acction request with without cookies and without token:")
        # action_request = requests.post('http://127.0.0.1:5000/api/action')
        # print(action_request.status_code, action_request.reason, action_request.content)

        # print("")
        # print("make acction request with cookies and without token:")
        # action_request = requests.post('http://127.0.0.1:5000/api/action', headers=headers)
        # print(action_request.status_code, action_request.reason, action_request.content)

        # print("")
        # print("make acction request with token and without cookies:")
        # action_request = requests.post('http://127.0.0.1:5000/api/action', cookies=cookies)
        # print(action_request.status_code, action_request.reason, action_request.content)

        # print("")
        # print("make acction request with cookies and token:")
        # action_request = requests.post('http://127.0.0.1:5000/api/action', headers=headers, cookies=cookies)
        # print(action_request.status_code, action_request.reason, action_request.content)
