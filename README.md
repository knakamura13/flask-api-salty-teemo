# flask-api-salty-teemo
An API for various Salty Teemo information

## Endpoints

`/live-data [GET|POST|PUT]`

Example response
```json
{
  "live_stats": {
    "betting_is_open": false,
    "blue": {
      "bets": 19,
      "mushrooms": 44291,
      "name": "blue"
    },
    "latest_update": "2021-03-22 19:22:42",
    "red": {
      "bets": 19,
      "mushrooms": 106283,
      "name": "red"
    },
    "total": {
      "bets": 38,
      "mushrooms": 150574
    }
  },
  "status": 201,
  "status_code": 200
}
```
