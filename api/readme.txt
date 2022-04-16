startup:
uvicorn main:app --host=0.0.0.0 --port=8080

use:
GET http://<host>:8080/entrant/<entrant-id>

Verus CSV endpoint based on [code](https://gist.github.com/its-dron/bce1cc4581ac8a56f4c4dd73aefc5137) provided by [DRON](https://github.com/its-dron).