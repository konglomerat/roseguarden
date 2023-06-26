
# Node actions requested by the server

!!! important "The description of this actions is written from the perspektive of action-requests by the server. <br> The actions meant to be executed by the node and will be a send in form of a request-reply by the node." 

## General actions

This actions every node should implement.
The node have to reply to this general actions send by the server.

### Identify ( sendIdentification )

Request the node to send a `syncNodeIdentification` action to the server.

### Get node log ( sendLogs )

**Example:**


The node should send a list of `updateNodeLog`-actions to the server.
The actions contains actual history informations. The last n (min. 5) actions have to be stored in the nodes ram.
The history wont be reset after send.

``` json
{
    "head" : {
        ...
    },
    "actions" : [
        {
            "action" : "updateNodeLog",          
            "logid" : 22,
            "logaction" : "openDoor",          
            "timestamp" : "2020-03-24T20:21:58+01:00",
            "source" : "roseguarden.fabba.space"
        },        
        {
            "action" : "updateNodeLog",          
            "logid" : 21,
            "logaction" : "readRfid", 
            "timestamp" : "2020-03-24T20:22:58+01:00",
            "source" : "internal"
        },
    ],
}
```

### Update settings ( updateSettings )

The server will send a action to update the list of node settings.
The action contain all properties

E.g.: 

``` json
    "head" : {
        ...
    },
    "actions" : [
        {
            "action": "updateSettings",
            "settingA": "a",
            "settingB": "b"
        }
    ]
```

The list can be empty to trigger a `syncNodeSettings`-action with the actual possible settings avalable.

``` json 
    "head" : {
        ...
    },
    "actions" : [
        {
            "action": "updateSettings",       
        }
    ]
```



The node have to respond with a `syncNodeSettings`-action to the server.

E.g.:

``` json
    "head" : {
        ...
    },
    "actions" : [
        {
            "action": "syncNodeSettings",
            "settingA": "a",
            "settingB": "b"                 
        }
    ]
```

### Trigger neighbour ( triggerNeighbour )


## Node specific actions 

* [For door node](doornodesactions.md)
