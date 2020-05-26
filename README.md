# First REST-API 

# 1. Query Hotels

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

# 2. User Registration

## Request

Example request to register a new user.

**Method**: `POST`

**URL**: `/register`

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

# 3. User Login

DOING...