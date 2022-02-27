# resources database spec

# resources
each resource will need a resource `id`, a string for the resource `name` this will be formatted as a json object

# linking players to resources
a table will be needed to link players to their resources, this will need a `player uid`, a `resources uid`, and an `amount` of that resource. this table will be updated frequently whenever the player gets or uses resources

# linking resources to locations
each location will have to be linked to a resource, this will be done using a table containing a `location id` and a `resource id`, and an `amount` for that location. this table will be able to be updated frequently to change what resources are available at each location