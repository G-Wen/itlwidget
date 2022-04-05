startup:
uvicorn main:app --host=0.0.0.0 --port=8080

use:
GET http://<host>:8080/entrant/<entrant-id>
