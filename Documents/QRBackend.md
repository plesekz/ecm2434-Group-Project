# QR Backend Specification Document
## The Four Endpoints
- `/createRes`-- Whenever this is requested, the server will create a new resource.
- `/deleteRes` -- Whenever this is requested, the server will delete a certain resource.
- `/retrieveRes` -- Whenever this is requested, the server will retrieve a certain resource.
- `/listRes` -- Whenever this is requested, the server will list all resources.

## The Resource Fields
All resources will have the following attributes:
- `codeID`(A 5-digit ID that refers to the exact resource that has been created)
- `resource` (A list of all `type` and `amount` that the resource contains)
	- `type` (A 3-Digit ID that refers to the the type of resource to be created e.g. "001" refers to Wood)
	- `amount` (An integer that denotes how much of the resource is to be created)
- `latitude` (A decimal that denotes the lattitude of where the resource QR code will be placed)
- `longitude` (A decimal that denotes the longitude of where the resource QR code will be placed)

## `/createRes`
This is a game master and admin-level only command. This should create a JSON object within the database with all the attributes listed above. Note that a single resource may contain multiple resource types (as shown below).

The `createRes` view will be mapped to the `/createRes` URL path.

To send the data, the client must **POST** a **raw JSON object** to **`/createRes`**. This will then be decoded on the server, and saved into the database.** Upon a successful creation, the server replies with a HTTP code 200, else 400.**

**Unsure whether the generation of a sequential/random codeID should be done client-side or on server. Assuming codeID is generated client-side, the following JSON object may be POSTed:**
```
{
  "codeID": "12345",
  "resource: "{
    "type": "001",
    "amount": "3"
  }, {
    "resourceType": "002",
    "amount": "3"
  }",
  "latitude": "50.736",
  "longitude": "-3.532"
}
```
This JSON object indicates there a resource of codeID "12345" contains 3 of two types of resources, "001" and "002". The latitude and longitude are self-explanatory.


## `/deleteRes`
This is a game master and admin-level only command. We can delete a resource based off its codeID. The view should iterate the database of JSONs by resourceIDs and upon finding it, remove it from the database.

The `deleteRes` view will be mapped to the `/deleteRes` URL path.

To send the data, the client must **POST** the **codeID** as an **IntegerField** (of length 5) to **`/deleteRes`**.** Upon successful deletion, the server replies with a HTTP code 200, else 400.**

## `/retrieveRes`
This is a player-level command. As all resources have unique IDs, we can retrieve JSON objects from the database using this. Similar to `deleteRes`, this view should search the database by codeIDs and upon finding the matching resource, should return it. It should not delete the object from the database.

The `retrieveRes` view will be mapped to the `/retrieveRes` URL path.

To send the data, the client must **POST** the **codeID** as an **IntegerField** (of length 5) to **`/retrieveRes`**.** If retrieval is unsuccessful, the server replies with a HTTP 400.**


## `/listRes`
This is a game master and admin-level command. We can return all resources, as JSON objects, that we have stored in our databases.

Although this view will iterate through the database like `deleteRes` and `retrieveRes`, it will not search for a specific resource unlike the other two. Each resource will instead be appended to a list as a JSON object which will finally be returned.

The `listRes` view will be mapped to the **`/listRes`** URL path. Simply visiting this URL will trigger the view. **If retrieval is unsuccessful, the server replies with a HTTP 400.**
