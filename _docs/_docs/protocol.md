# Protocol

* the protocol based on https-requests
* the data will be send/received as json container 
* the server is meant to be master and synchronize every client or node
* the protocol based on an action based pattern, every requests contains actions that should be executed by the receiver
* every request to the server will be responded by a list of actions for the sender (client or node)
* the list of actions of a server-response are meant to be executed on the client/node
* events on the clients or node will trigger action-requests to the server

## General request structure

An example from the (web-)client to the server:

``` json
{
    "head" : {
        "version" : "1.0.0",
        "target" : "roseguarden.fabba.space",
        "source" : "Username",
        "sourcetype" : "client",        
        "timestamp" : "2020-03-24T20:20:58+01:00"
    },
    "actions" : [
        {
            "version" : "1.0.0",
            "action" : "executeViewAction",
            "workspace" : "users",
            "view" : "userList",
            "viewAction" : "lock",
            "entry" : {
                "email" : "test@test.de",
                "name" : "testuser",
            }
        }
    ]
}
```

An example from the node to the server:

``` json
{
    "head" : {
        "version" : "1.0.0",
        "target" : "roseguarden.fabba.space",
        "source" : "Nodename",
        "sourcetype" : "door",
        "fingerprint" : "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1",
        "authentification" : "Kol-Bi-Hop-Ban-Gan-To-Sep+129",
        "timestamp" : "2020-03-24T20:20:58+01:00",
        "uptime": 0,
        "logcounter": 0,
        "errorcounter": 0,        
    },
    "actions" : [
        {
            "version" : "1.0",
            "action" : "requestNodeUpdate",
            "actionid" : 8          
        },
    ],
}
```

## General head properties

The `head` section in a request, contains static information of the sender that are not bind to specific action.

### Version

The version in `head` shows the protocol version.
Will be ignored at the moment and dont have to be set (string version number, e.g. "1.0.0")

### Target

The target of the request.
Will be ignored at the moment and dont have to be set.
Could be set to "server.url.tld" (for a request to a server) or "nodename" (for a request to a node).

### Source

The source of the request.
Is needed to identify the requester.

Set to "nodename" for a request to a server.
Set to "server.url.tld" (for a reply to a node)

### Sourcetype

The type of source the request/reply come from.
Is needed to identify the requester.
Will be ignored at the moment and dont have to be set.

Could be "client", "door-node", "server".

### Timestamp

The `timestamp` property show the actual time of the device.
Will be ignored at the moment but have to be set to any datestring value in the form of `2020-03-24T20:20:58+01:00`.


## Node specific head properties

### Node fingerprint

The `fingerprint` property have to be set to identify the node.
The property is a string e.g. in the form of an SHA-1 (160bit) hash in the form of  "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1".

### Node authentification

The `authentification` property have to be set to authenticate the node.
The property is a string e.g. "Kol-Bi-Hop-Ban-Gan-To-Sep+129" (no further restricitions, like length at the moment).

### Node uptime


The `uptime` property have to be set to register startups.
The value should be in seconds since startup.

### Node logging counter

The `logcounter` property have to be set to show the number of present log entries. 
The property will be ignored at the moment but have to be set to any value (e.g. 0).

### Node error counter

The `errorcounter` property have to be set to inform about errors occure at node runtime.
The property will be ignored at the moment but have to be set to any value (e.g. 0).

## Actions

The `actions` section contain a list of actions that should be executed by the receiver of the request.

An example:
 
``` json
    "actions" : [
        {
            "version" : "1.0.0",
            "action" : "requestNodeUpdate",
            "actionid" : 8          
        },
```

### Version

The `version` property in an action entry shows the action version requested.
Will be ignored at the moment and dont have to be set (string value). 
Could be set to "1.0.0".

### Action ID

The `actionid` property in an action entry identify the action.
The value should be incremented for every action requested to be unique.
The property-value should be an integer.

### Specific actions for nodes and clients

See the pages for specific actions for [node](nodeactions.md) and [client](clientactions.md) to get further information and a list of available action on each. Have a look at the [minimal node implementation](minimal.md) for a door

## Optionals

In addition to `head` and `action` there could be optional sections to customize to your needs. There is no strict checking. 
