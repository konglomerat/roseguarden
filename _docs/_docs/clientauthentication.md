# Authentication for clients

To autheticate clients (e.g. browser) JWTs (JSON web token)  are used.
On the backend the `flak-jwt-extended' module is used.
The JWT is stored in the http/s header `Authorization`. The header type is `Bearer`.
