# Minimal node implementation

This is a minimum example for getting a door (node) running.

## Action requests to be send to the server after an event 

The following events have to be handled by the node:

### Send an startup information

Event: On Startup

Action: Send a `registerNodeStartup` request to the server to inform about the startup.

**Example of the registerNodeStartup request to send:**

``` json
    {
    "header": {
        "source": "Door 1",
        "version": "1.0.0",
        "target": "roseguarden.fabba.space",
        "fingerprint": "33:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1",
        "authentification": "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
        "uptime": 0,
        "logcounter": 0,
        "errorcounter": 0,
        "timestamp": "2021-01-29T09:46:52.594Z"
    },
    "actions": [
            {
                "version": "1.0.0",
                "action": "registerNodeStartup",
                "actionid": 8
            }
        ]
    }
```

### Get an update from the server (heartbeat) every 1 minute

Event: Every 1 minute

Action: Send a `requestNodeUpdate` request to the server

**Example of the requestNodeUpdate request to send:**

``` json
    {
    "header": {
        "source": "Door 1",
        "version": "1.0.0",
        "target": "roseguarden.fabba.space",
        "fingerprint": "33:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1",
        "authentification": "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
        "uptime": 0,
        "logcounter": 0,
        "errorcounter": 0,
        "timestamp": "2021-01-29T09:46:52.594Z"
    },
    "actions": [
            {
                "version": "1.0.0",
                "action": "requestNodeUp date",
                "actionid": 8
            }
        ]
    }
```

### Request user access 

Event: when a authenticator appears (rfid)

Action: The node should request access for the user by sending a `requestUserAccess` action request to the server.

**Example of the requestUserAccess request to send:**

``` json
  "actions": [
    {
      "version": "1.0.0",
      "action": "requestUserAccess",
      "actionid": 11,
      "pin": "111111",
      "auth_key": "112.123.23.1.91"
    }
  ]
```

**Authentication key property:**

The authetication key (`auth_key`) given from the authenticator (rfid).
The property value have to be a string.

**PIN property (optional):**

An optional `pin` in addition to the `auth_key`.
The property value have to be a string with the given pin.


### Request a assign code when a authenticator appear

Event: when a authenticator appears (rfid) and assign mode is active

Action: The node should request a assign code for the user by sending a `requestAssignCode` action request to the server.

**Example of the requestAssignCode request to send:**

``` json 
  "actions": [
    {
      "version": "1.0.0",
      "action": "requestAssignCode",
      "actionid": 2,
      "auth_key": "112.123.23.1.91"
    }
  ]
```      
    
**Authentication key property:**

The authetication key (`auth_key`) given from the authenticator (rfid).
The property value have to be a string.


## Action requests from the server a node have to handle

The following actions have to be handled by the server after requested by the server on startup or after any action request:

### Send node identification

The node have to handle requested `sendIdentification` actions.
The action request an indetification of the node which is unknwon to the server.
The server expect a `syncNodeIdentification` action request to be send.
Until the identification was successfull (done by the administrators) every further action request will be replied with a request to send the nodes identification.  

Have a look at the [Sync. the node identification ( syncNodeIdentification ) section](servernodeactions.md) how to send a valid `syncNodeIdentification` action request.

**Example of the requested action:**

``` json
  "actions": [
    {
      "action": "sendIdentification",
      "version": "1.0.0"
    }
  ]
```

### Grand access to open the door

The node have to handle requested `grandAccess` actions.
This action opens the door and show some user information.

**Example of the requested action:**

``` json
  "actions": [
    {
      "action": "grandAccess",
      "version": "1.0.0",
      "message": "Welcome",
      "info": "Test Admin\n"
    }
  ]
```   

**Message property:**

The message to show

**Info property:**

Further infos to show.


### Deny access to open the door

The node have to handle requested `denyAccess` actions.
This action deny the door opening and show some informations for that.

**Example of the requested action:**

``` json
  "actions": [
    {
      "action": "denyAccess",
      "version": "1.0.0",
      "message": "Wrong pin",
      "info": "Remaining attempts: 5"
    }
  ]
``` 

**Message property:**

The message to show

**Info property:**

Further infos to show.

### Show/update the assign info

The node have to handle requested `updateAssignInfo` actions.

**Example of the requested action:**

``` json
  "actions": [
    {
      "action": "updateAssignInfo",
      "version": "1.0.0",
      "code": "21:B3:87:2D:88:98",
      "valid": true
    }
  ]
``` 

**Valid property:**

Shows if the assign was succesfull.

**Code property:**

The assign code to show to the user
