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
	* min_daily &rarr; Minimum daily rate from R $ 0 to R $ 10,000.00. 
		* Default: 0
	* max_daily &rarr; Maximum daily rate of the hotel from R $ 0 to R $ 10,000.00. 
		* Standard: 10000
	* limit &rarr; Maximum number of elements displayed per page. 
		* Default: 50
	* offset &rarr; Number of elements to skip (usually multiple of limit). 
		* Default: 0

<!-- table -->
<!-- | **Method** | **URL** | **Authorization required**
|:-----------|:--------|:--------------------------
|`GET`		 |`/hotels`|NO		 -->

**URL**: `/hotels?city=Santos&min_stars=1.0&max_stars=3.0&max_daily=700&limits=10`

**Method**: `GET`

**Authorization required**: NO

## Success Response

**Code** : `200 OK`

**Content example**

As an answer, get a list of hotels that fit the requisition filters above:

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

## Request

Request to view data for a specific hotel. A GET is made of `/hotels/{hotel_id}`

**URL**: `/hotels/bravo`

**Method**: `GET`

**Authorization required**: NO

## Success Response

**Code** : `200 OK`

**Content example**

As an answer, get a list of hotels that fit the requisition filters above:

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

TODO

# TEMPLATE EXAMPLE

# Login

Used to collect a Token for a registered User.

**URL** : `/api/login/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "iloveauth@example.com",
    "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "non_field_errors": [
        "Unable to login with provided credentials."
    ]
}
```
