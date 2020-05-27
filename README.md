# First REST-API 

# 1. Query Sites

## Request

Request to return all sites in the system

**Method**: `POST`

**URL**: `/sites`

**Authorization required**: NO

**No Body**

## Response

As response, you get a message saying that the user was not found.

**Code** : `200 OK`

**Response Body**:
```json
{
  "sites": [
    {
      "site_id": 1,
      "url": "www.test1.com",
      "hotels": [
        {
          "hotel_id": "alpha",
          "name": "Alpha Hotel",
          "stars": 3.4,
          "daily": 661.92,
          "city": "Santos",
          "site_id": 1
        },
        {
          "hotel_id": "fox",
          "name": "Fox Hotel",
          "stars": 5.0,
          "daily": 123.92,
          "city": "Santos",
          "site_id": 1
        }
      ]
    },
    {
      "site_id": 2,
      "url": "www.test2.com",
      "hotels": [
        {
          "hotel_id": "gama",
          "name": "Gama Hotel",
          "stars": 3.3,
          "daily": 346.92,
          "city": "Rio de Janeiro",
          "site_id": 2
        }
      ]
    },
    {
      "site_id": 3,
      "url": "www.test3.com",
      "hotels": []
    },
    {
      "site_id": 4,
      "url": "www.test4.com",
      "hotels": [
        {
          "hotel_id": "delta",
          "name": "Delta Hotel",
          "stars": 1.2,
          "daily": 955.92,
          "city": "Rio de Janeiro",
          "site_id": 4
        },
        {
          "hotel_id": "eagle",
          "name": "Eagle Hotel",
          "stars": 4.5,
          "daily": 512.1,
          "city": "São Paulo",
          "site_id": 4
        }
      ]
    },
    {
      "site_id": 5,
      "url": "www.test5.com",
      "hotels": []
    }
  ]
}
```
---

## Request

Example request a single site: `/sites/{url}`

**Method**: `POST`

**URL**: `/sites/www.test1.com`

**No Body**

## Response

As response, you get info about the url.

**Code** : `200 OK`

**Response Body**:
```json
{
  "site_id": 1,
  "url": "www.test1.com",
  "hotels": [
    {
      "hotel_id": "alpha",
      "name": "Alpha Hotel",
      "stars": 3.4,
      "daily": 661.92,
      "city": "Santos",
      "site_id": 1
    },
    {
      "hotel_id": "fox",
      "name": "Fox Hotel",
      "stars": 5.0,
      "daily": 123.92,
      "city": "Santos",
      "site_id": 1
    }
  ]
}
```
---

## Request

Example request a site that not exists in system.

**Method**: `POST`

**URL**: `/sites/www.not_exists.com`

**No Body**

## Response

As response, you get a message saying that the site was not found.

**Code** : `404 Not Found`

**Response Body**:
```json
{
  "message": "site 'www.not_exists.com' not found!"
}
```
---


# 2. Query Hotels

## Request

Request to list all hotels in the system, with the option of receiving customized filters
via path, so that if the customer does not define any query parameters (no filters), the
parameters will receive the default values.

* Possible query parameters:
	* city &rarr; Filter hotels by the chosen city. 	
		* Default: Null
	* min_stars &rarr; Minimum hotel ratings from 0 to 5. 
		* Default: 0
	* max_stars &rarr; Maximum hotel ratings from 0 to 5. 
		* Default: 5
	* min_daily &rarr; Minimum daily value from 0 to 10000. 
		* Default: 0
	* max_daily &rarr; Maximum daily value from 0 to 10000. 
		* Default: 10000
	* limit &rarr; Maximum number of elements displayed per page. 
		* Default: 50
	* offset &rarr; Number of elements to skip (usually multiple of limit). 
		* Default: 0

**Method**: `GET`

**URL**: `/hotels?city=Santos&min_stars=1.0&max_stars=3.0&max_daily=700&limits=10`

**Authorization required**: NO

## Response

**Code** : `200 OK`

**Response Body**

As response, is obtained a list of hotels that fit the requisition filters above:

```json
{
  "hotels": [
    {
      "hotel_id": "bravo",
      "name": "bravo Hotel",
      "stars": 2.3,
      "daily": 661.92,
      "city": "Santos",
      "site_id": 2
    },
    {
      "hotel_id": "new",
      "name": "new Hotel",
      "stars": 1.0,
      "daily": 661.92,
      "city": "Santos",
      "site_id": 4
    },
    {
      "hotel_id": "after_session",
      "name": "after session Hotel",
      "stars": 1.0,
      "daily": 661.92,
      "city": "Santos",
      "site_id": 4
    }
  ]
}
```

---

## Request

Request to view data for a specific hotel. A GET is made of `/hotels/{hotel_id}`

**Method**: `GET`

**URL**: `/hotels/bravo`

**Authorization required**: NO

## Response

**Code** : `200 OK`

**Response Body**

As response, is obtained a JSON with the data of requested hotel:

```json
{
  "hotel_id": "bravo",
  "name": "bravo Hotel",
  "stars": 2.3,
  "daily": 661.92,
  "city": "Santos",
  "site_id": 2
}
```

---

## Request

Request of a hotel that not exists

**Method**: `GET`

**URL**: `/hotels/not_exists`

**Authorization required**: NO

## Response

**Code** : `404 Not Found`

**Response Body**

As response, a message is obtained saying that the hotel was not found:

```json
{
  "message": "hotel 'not_exists' not found."
}
```

# 3. User Registration

## Request

Example request to register a new user.

**Method**: `POST`

**URL**: `/register`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel",
  "password": "123",
  "email": "daniel@email.com"
}
```

## Response

As response, you get a success message that the user was created and an message is sent to your email for you active this account.

**Code** : `201 Created`

**Response Body**:
```json
{
  "message": "user 'danbailo' has been created successfully!"
}
```

---

## Request

Example request to register a new user with same login.

**Method**: `POST`

**URL**: `/register`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel",
  "password": "123",
  "email": "other_email@email.com"
}
```

## Response

As response, you get a message saying that the login already exists.

**Code** : `404 Bad Request`

**Response Body**:
```json
{
  "message": "The login 'daniel' already exists."
}
```

---

## Request

Example request to register a new user with same email.

**Method**: `POST`

**URL**: `/register`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel",
  "password": "123",
  "email": "other_email@email.com"
}
```

## Response

As response, you get a message saying that the email already exists.

**Code** : `404 Bad Request`

**Response Body**:
```json
{
  "message": "The email 'daniel@email.com' already exists."
}
```
---

# 4. User Login

## Request

Example request to login after create account.

**Method**: `POST`

**URL**: `/login`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel",
  "password": "123",
}
```

## Response

As response, you get a `access token` to access other resoures when Authorization is needed.

**Code** : `200 OK`

**Response Body**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA1NDc5MjQsIm5iZiI6MTU5MDU0NzkyNCwianRpIjoiZjVmYzNmNjItNGYwZC00ODc3LWEzNjctOGFjZDEzMGJkZjU4IiwiZXhwIjoxNTkwNTUxNTI0LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.BAUrmy4X_h0TTerkqrPV3adTJSd1k_VqFWGc-2bKgJY"
}
```
---

## Request

Example request to login after create account but it is not confirmed.

**Method**: `POST`

**URL**: `/login`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel_not_confirmed",
  "password": "123",
}
```

## Response

As response, you get a message saying that the user was not confirmed.

**Code** : `401 Unauthorized`

**Response Body**:
```json
{
  "message": "user 'daniel_not_confirmed' is not confirmed."
}
```
---

## Request

Example request to login when the account was not created.

**Method**: `POST`

**URL**: `/login`

**Authorization required**: NO

**Request Header**
  * `Content-type`: `application/json`

**Request Body**:
```json
{
  "login": "daniel_not_created",
  "password": "123",
}
```

## Response

As response, you get a message saying that the user was not found.

**Code** : `401 Unauthorized`

**Response Body**:
```json
{
  "message": "user 'daniel_not_created' not found."
}
```
---

# 4. Create Site

## Request

Example request to create a site: `/sites/{url}`.

**Method**: `POST`

**URL**: `/sites/www.test.com`

**Authorization required**: NO

**No Body**

## Response

As response, you get a message showing the info about the new entry, such as site_id, url and the hotels.

**Code** : `401 Unauthorized`

**Response Body**:
```json
{
  "site_id": 1,
  "url": "www.test.com",
  "hotels": []
}
```
---

# 6. Create Hotel

## Request

Example request to create a new hotel `/hotels/{hotel_id}`

**Method**: `POST`

**URL**: `/hotels/test`

**Authorization required**: YES

**Request Header**
  * `Content-type`: `application/json`
  * `Authorization`: `Bearer {access_token}`

**Request Body**:
```json
{
  "name": "test hotel",
  "stars": 3.4,
  "daily": 661.92,
  "city": "Santos",
	"site_id": 1
}
```

## Response

As response, you get a message saying that the user was not found.

**Code** : `401 Unauthorized`

**Response Body**:
```json
{
  "message": "user 'daniel_not_created' not found."
}
```
---