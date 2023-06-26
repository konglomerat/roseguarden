# Authentication for nodes

The nodes have a different authetification than the client. A node sends a secret `nodeauth` in every action request to authenticate itself to the server. The `nodeauth` is stored in the `header` section. To exchange and validate the authentification token a process using the AES is implemented. To secure the nodes from captured network or man in the middle attacks the server will authenticate himself with a token `serverauth`.

!!! info "The nodes communicate by the https-api with a valid certificate 

## Background imformations

* the server has a secret key stored in the system configiguration (config.ini) called `serversecret`
* the `serversecret` have to be secret and unique for every roseguarden instance
* the node has a secret key (`ǹodesecret`) and a public fingerprint (`fingerprint`) flashed into the memory
* the `ǹodesecret` as well as the `fingerprint` have to be unique and different for every roseguarden instance
* the nodes use a unique cipher (`nodecipher`) for authentication that will be requested from the server by an action-request
* the `nodecipher` is created by the server encoding the nodes `fingerprint` with the `serversecret` as the key
* only a hash of it got stored (`nodeauth`), not the `nodecipher` itself,
* the `nodeauth` is the AES enconded `nodecypher` with the `nodesecret` as the key
* the `serverauth` is the AES encoded `fingerprint` with the `nodesecret` as the key
* actions to a nodes only are executed with a valid `serverauth` (except authetification actions)
* the AES algorithm need a key and an intitialisation vector (iv) to work
* the iv is a random cipher created at the startup of the server
* the public iv need to be distributed from the server to the nodes (`nodeiv`)


## Exchange and validate the secret (on setup)

* On setup there is are the following prerequisite:
    * the node stores a `ǹodesecret` (flash, AES encrypted)
    * the node stores a `fingerprint` (flash, AES encrypted)
    * the node stores a **unvalid** `nodecipher` (flash, AES encrypted), e.g. the `nodecipher` is empty (`nodecipher = ""`)
    * the node dont have a `nodeiv` (ram)
* when the `nodecipher` is empty, the node will send an empty `nodeauth` (`"nodeauth" : ""`) on requests, e.g. while sending the updateNode or registerStartup action
* the server will respond to an empty `nodeauth` with an `authenticate` action request
* the node will reply the `authenticate` action request with an `authorizenode` action request with the following parameters:
    * the `fingerprint` of the node
    * the actual `nodeiv`
* the server will add node to the authorize request list and wait for manual authorization e.g. by the admin on the web-ui
    * the admin check the authorization request and the fingerprint
    * the admin enter the `ǹodesecret` to generate the`serverauth` and the  `nodecipher` for the node and store it securely on the server
    * the `ǹodesecret` will not be stored
* after manual authorization the server will respond to a action request of the node with a `updateauthorization` with the following parameters:
    * `nodecipher` to be stored by the node into the flash
    * `nodeiv` to be stored by the node into the ram
* a node is able to generate and use the `nodeauth` for every communication now
* a node is able to check the specific `serverauth` for every action requested by the server now

## Verification after node restart

After node restart the node don't know the actual initializaion table of the server (`nodeiv = ""`)

* An empty `nodeauth` will send for requests (`"nodeauth" : ""`)
* the server will respond to an empty `nodeauth` with a `authenticate` action request
* the node will reply the `authenticate` action request with an `authorizenode` action request with the following parameters:
    * the `fingerprint` of the node
    * the actual `nodeiv`
* the server will respond to a action request of the node with a `updateauthorization` with the following parameters:
    * `nodeiv` to be stored by the node into the ram
    * **no** new `nodecipher` will be send, for `authenticate` action request with an empty `nodeiv`
* a valid node with correct `nodecipher` will work again

## Verification after server restart

## Verification after replacing a node

* even with the same `nodesecret` and `fingerprint` no `nodecipher` (is empty) is available on the node
* The node have to be add like an unitialized node have a look at "Exchange and validate the secret (on setup)"

## Verification after server and node get restarted at the same time

## Considered attacks

!!! info "Assupmtions to secureness of nodes and server"
It shall be assumted that the server is secure. Either the `serversecret` and the `serverauth` on the server as well as the `nodesecret` and `nodecipher` on the nodes have to been kept secret from any attacker. If the private keys leaked or the attacker got access to the server-data the system gets vulnerable to further attacks.

### Faked server (like in captured networks or man in the middle attacks)

* to the secure the communication HTTPS with a valid certificate is used

### Faked nodes

* to the secure the communication HTTPS with a valid certificate is used

## Not safe?

We do our best to keep roseguarden safe from attacks of all kind. We considered all principles of data security and authetification mechanism we know.
Of course we are no professionals for security implementation. If you find some weak point in our authetification mechanism, please contact us to improve the security of the system.