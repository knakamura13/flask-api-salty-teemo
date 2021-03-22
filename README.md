# flask-api-salty-teemo
An API for various Salty Teemo information

## API Usage

**Base URL**

https://flask-api-salty-teemo.herokuapp.com

**Endpoints**

`/live-data [GET|PUT|POST]`

**Sample requests**

```
GET /live-data HTTP/1.1
Host: flask-api-salty-teemo.herokuapp.com
```

```
PUT /live-data HTTP/1.1
Host: flask-api-salty-teemo.herokuapp.com
Content-Type: application/json
Content-Length: 298

{
    "live_stats": {
        "betting_is_open": true,
        "blue": {
            "bets": 1,
            "mushrooms": 1
        },
        "red": {
            "bets": 1,
            "mushrooms": 1
        },
        "total": {
            "bets": 1,
            "mushrooms": 1
        }
    }
}
```

```
POST /live-data HTTP/1.1
Host: flask-api-salty-teemo.herokuapp.com
Content-Type: application/json
Content-Length: 365

{
    "live_stats": {
        "betting_is_open": true,
        "blue": {
            "bets": 1,
            "mushrooms": 1
        },
        "latest_update": "2021-02-26 04:54:03",
        "red": {
            "bets": 1,
            "mushrooms": 1
        },
        "total": {
            "bets": 1,
            "mushrooms": 1
        }
    },
    "status": 201
}
```

**Sample response**

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
