# Design exercise: Fast flower delivery

## Scenario

The flower stores in a large city have established an agreement with local independent van drivers to deliver flowers from the city's flower stores to their destinations.

When a store gets a flower delivery order, it creates a request and broadcasts the request to qualified drivers within a certain distance from the store. The request includes the time for pick up (typically now) and the required delivery time for urgent deliveries.

A driver is then assigned and the customer is notified that a delivery has been scheduled.

The assigned driver picks up the delivery and delivers it, and then person receiving the flowers confirms the delivery time using an app on the driver's mobile device.

The system maintains a ranking of each individual driver based on his or her ability to deliver flowers on time.

Each store has a profile that can include a constraint on the ranking of its drivers, for example a store can require its driver to have a ranking greater than a certain value when they make the delivery request.

The profile also indicates whether the store wants the system to assign drivers automatically, or whether it wants to receive several bids and then make its own choice.

# Do This

For each of the following steps, use whatever documentation technique that you think will communicate your design. 

1. Write down four primary user stories for Fast Flower Delivery. A user story is one sentence that describes someone doing something to something or someone else. For example, a user story for an ecommerce Web site might be "Customer adds item to shopping cart." Avoid generic names like "user" and use specific names like "customer" instead. Do not do any user stories for logging in, logging out, etc. 
2. Describe a data model that supports the user stories you created in (1). What data needs to be stored and how is it structured?
3. Design an API for the data model and user stories in (2) and (3). Note that this doesn't have to be a complete API, just enough to support your user stories. 

# Deliverables

Turn in

1. Your user stories. 
2. A diagram of the model. 
3. A Swagger file for the API you designed above. You should use the Swagger editor at swagger.io to create it.



