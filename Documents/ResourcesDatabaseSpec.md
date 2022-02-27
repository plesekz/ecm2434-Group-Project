# resources database spec

# resources
each resource will need a resource `id` (int) (primary key), a resource `name` (string).

# linking players to resources
a table will be needed to link players to their resources, this will need a `player uid` (foreign key int), a `resources uid` (foreign key int), and an `amount` (int) of that resource. this table will be updated frequently whenever the player gets or uses resources

# linking resources to locations
each location will have to be linked to a resource, this will be done using a table containing a `location id` (foreign key int) and a `resource id` (forgien key int), and an `amount` (int) for that location. this table will be able to be updated frequently to change what resources are available at each location