# Lab 2: Events, Event Generation, and Multi-Tenancy

**Objective:** Introduce the concepts of events, event signal URLs (ESLs), and registration. 

Before you start implementing, read the Evented API Specification (http://www.eventedapi.org/spec). You will be implementing the Generator portion of that specification in this lab. 

# Flower Shop website
Build a website to represent the Flower Shop owners.

- The site should support multi-tenancy. You will have accounts for an administrator (the flower shop owner) and users (the drivers).
- Add a form that delivery drivers can use (once they are logged in) to register their event signal URL (ESL) and other information with the flower shop.
- Add a form that the owner can use to submit a request for delivery.
- When a request for delivery is made, signal the event to every registered delivery driver via their ESL.

For this lab, you can create an ESL for each driver using the Example Event Consumer (linked below). You will implement your own event consumer in the next lab.

# Signaling events
You will be signaling one event in this lab. The event domain and name must be the following:

- Event domain: **rfq**
- Event name: **delivery_ready**

That event will need several attributes, such as the following:

- Address of the flower shop
- Pickup time (may be now or some time in the future)
- Delivery address
- Delivery time (if the delivery is urgent; otherwise you could leave this unspecified)

# Objective
When you have successfully completed this lab you will be able to:

1. Create event signal URLs (ESLs) using the Example Event Consumer (see below) and register them with the Flower Shop.
2. Fill out the form indicating a delivery is needed and see the resulting **rfq:delivery_ready** event along with the attributes at the Example Event Consumer.

# Implementation notes

- Signaling an event requires making an HTTP call to the ESL. The event is signaled whenever a flower shop owner completes the deliver form. Some attributes come from the form and others are hard coded or configured elsewhere in the Flower Shop site.
- Registering an ESL implies that the ESL and related information will be held persistently by the Flower Shop site.
- The _other information_ that is registered with the ESL should contain at least the name of the driver. As you progress in the project, you may discover that you need additional information, so implement the registration form in a flexible manner that allows for future expansion.

# Resources
The following sites will be a great help in testing your site and learning how the events should be signaled:

- [Example Event Generator](http://generator.eventedapi.org/) (for generating events and sending them to any URL)
- [Example Event Consumer](http://consumer.eventedapi.org/) (for receiving events from any generator)
- [Postbin](http://postbin.org/) (for inspecting HTTP POST requests)

# Grading

- 20% &mdash; Multiple accounts of the proper types supported
- 20% &mdash; Driver and ESL registration
- 20% &mdash; Delivery request form
- 40% &mdash; Proper event signaling

To pass off you will need to demonstrate to the TA by showing in person or email the Ip and aim # (if it's running on the Amazon cloud). 
