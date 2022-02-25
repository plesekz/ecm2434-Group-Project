# QR Backend Specification Document
----
## The QR backend is based on top of **four** endpoints.
`/createRes`-- Whenever this is requested, the server will create a new resource.\
`/deleteRes` -- Whenever this is requested, the server will delete a certain resource.\
`/retrieveRes` -- Whenever this is requested, the server will retrieve a certain resource.\
`/listRes` -- Whenever this is requested, the server will list all resources.

## `/createRes`
This is a game master and admin-level only command. As all resource-types will have an ID (in the form XXX) associated with them, when creating a resource, we may refer to it by its ID during the creation process.

Let us assume we have a resource 'Wood' with the ID 001, and we which to add 3 of these in the location (50.736, -3.532) (Outside the Amory Parker building) This may be passed in as `thegame.com/gm/createRes?res=001&amount=3&lat=50.736&long=-3.532/`.

The `createRes` view will be mapped to the `/createRes` URL path and will take in the arguments:
-- `res` (A 3-Digit ID that refers to the resource to be created)\
-- `amount` (An integer that denotes how much of the resource is to be created)\
-- `lat` (A decimal that denotes the lattitude of where the resource QR code will be placed)\
-- `long` (A decimal that denotes the longitude of where the resource QR code will be placed)

This should create a JSON object within the database with all these attributes **and** an additional UID for that specific resource. This will then be updated on the Resource Management System.

The JSON object will hold a similar structure to the one below:

```
{
  "UID": "12345",
  "resourceType": "001",
  "amount": "3",
  "latitude": "50.736",
  "longitude": "-3.532"
}
```

## `/deleteRes`
This is a game master and admin-level only command. We can delete a resource based off its UID.

Let us assume we wish to delete a resource with the UID '12345'. This may be passed in as `thegame.com/gm/deleteRes?UID=12345/`.

The `deleteRes` view will be mapped to the `/deleteRes` URL path and will take in the argument:
-- `UID` (a set of integers that denotes the unique identity of the resource to be deleted).

The view should iterate the database of JSONs by UIDs and upon finding it, remove it from the database.

## `/retrieveRes`
This is a player-level command. **I am unsure how to prevent a player simply typing in this URL and getting resources this way. Maybe hashing the URL or something? Or maybe I'm misunderstanding this and according to our plans, simply returning the JSON object isn't enough to add resources, and there's more validation that's required. Note: This spec assumes that geolocation validation has already taken place.** As all resources have unique IDs, we can retrieve JSON objects from the database using this.

Let us assume we wish to retrieve the JSON object associated with the resource with UID '12345'. This may be passed in as `thegame.com/p/retrieveRes?UID=12345/`.

The `retrieveRes` view will be mapped to the `/retrieveRes` URL path and will take in the argument:
-- `UID` (a set of integers that denotes the unique identity of the resource to be deleted).

Similar to `deleteRes`, this view should iterate the database of JSONs by UIDs and upon finding it, should return it. It should not delete the object from the database.

## `/listRes`
This is a game master and admin-level command. We can return all resources, as JSON objects, that we have stored in our databases.

Let us assume we wish to list all resources that we have created in our database. This may be passed in as `thegame.com/gm/listRes/`.

The `listRes` view will be mapped to the `/listRes` URL path and will not take in any arguments. It will return a list of JSON objects.

Although this view will iterate through the database like `deleteRes` and `retrieveRes`, it will not search for a specific resource unlike the other two. Each item will instead be appended to a list which will finally be returned.
