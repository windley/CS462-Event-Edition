# Lab 4: Event Intermediaries

**Objective:** Understand how intermediaries can be used in an event network. 

This lab introduces intermediaries in the form of a driver's Guild that represents drivers, keeps track of driver performance, and distributes **rfq:delivery_ready** events.

Event intermediaries simplify some interactions in event networks and cut down on the number point-to-point subscriptions that players must maintain. 

The following diagram shows how this will work:

![Lab 4 architecture](https://raw.githubusercontent.com/windley/CS462-Event-Edition/master/project-2013/Lab4-architecture.png)


---

# Driver's Guild

As you can see, the Driver's Guild is an organization that has it's own event network. 

- The Guild subscribes to flower shops so that it sees **rfq:delivery_ready** events
- The drivers subscribe to the Guild so that they see any **rfq:delivery_ready** events
- The Guild will maintain a universal identifier for each driver

The flowershops will send an **rfq:bid_awarded** event to the Guild with a driver ID to indicate they've selected a driver. The Guild is responsible for passing that to the driver who won. 

In addition, flower shops will signal a **delivery:picked_up** event to the Guild when the delivery is picked up. The event will need to include the driver identifier.

Drivers will signal a **delivery:complete** event to the Guild _and_ the flower shop when they have finished a delivery. 

The Guild will maintain a ranking of delivery drivers based on performance. 

When the Guild receives a **rfq:delivery_ready** event from a flower shop, it raises that event to the top three drivers based on performance (you can dummy up the data for testing purposes).  

The Guild is functioning as an event router, routing **rfq:delivery_ready** events to drivers as described above and **rfq:bid_awarded** events to the selected driver. 

---

# Drivers

In the diagram, we've shown the drivers sending **rfq:bid_available** events directly to the flower shops for two reasons:

1. The guild probably doesn't need to be involved in the bid process to do its job. 
2. You built this functionality in Lab 3 and there's no need to redo it here. 

That said, you might decide that the driver site will be simpler if drivers don't have to maintain a database of flower shops and ESLs.  There are two alternatives:

1. Have the guild intermediate the bid process as well. You'll need processes in the guild to handle and pass on **rfq:bid_available** events. 
2. Have the flowershop send a callback ESL as one of the attributes of the **rfq::delivery_ready**. The Driver doesn't know about flowershops, it simply uses the "return address" that the flowershop provides. 


The driver needs some way to notify his system when he has completed the actual delivery. You may use Twilio (as in Lab 3) or some other method.

---

# Implementation Notes

- Be careful not to use the guild as an excuse to over centralize logic. Flowershops and drivers still need to be independent. They are just intermediated by the guild. 
- You're free to determine how this ranking works. One possible solution is to base it on on-time performance for deliveries against a hypothetical best time. A production system would probably use a sophisticated service for this, but for our purposes, you can dummy up the ranking system and just update it with random performance rankings for each delivery. _Note:_ you **must** have a ranking system and update it, but it doesn't have to be "real."  Another way to think of this is you have to create the ranking API, but you don't have to put a real ranking algorithm behind it. 
- You may have the Guild intermediate **rfq:bid_available** events if you like. However, that is not required, and you'll need to justify your decision.
- In Lab 3, you had direct subscriptions from the flower shops to the drivers. You will need to undo those subscriptions. Drivers should now *only* see **rfq:delivery_ready** events from the Guild. 
- The universal driver identifier maintained by the Guild will need to be an attribute on any event referencing a driver. 
- You may need transaction IDs or some other identifier to link events about a particular delivery. 
- The diagram shows the driver sending **delivery:complete** events directly to the flowershop as well as the guild. You may choose to have the guild intermediate this event if it's easier. 
- The guild passes the **rfq:delivery_ready** to drivers. Use the ranking system to distribute the RFQ to the top three drivers. You may also need to take into account other information (like which driver's are available based on proximity to the shop, etc.). 
- When we say "the guild subscribes to the flowershops" don't assume that means the guild has to seek out flowershops and register with them. The word "subscribe" is meant to describe the direction that events flow, not how the registration process works. "The guild subscribes to the flowershops" means simply that the guild must provide the flowershop with an ESL. You could have flowershops come to the guild, register and get an ESL from the guild. 

---
#Exercises

*_N.B._ These are for in class use; you do _not_ have to turn them in with your project.*

0. Determine the event attributes for the new events introduced above. Also determine what changes will be necessary for the attributes of the **rfq:deliver_ready** and **rfq:bid_available** events. 
0. Draw an event hierarchy showing how events flow. Here's an <a href="http://www.flickr.com/photos/windley/5580410158/sizes/o/">example</a> of an event hierarchy. Use ovals for the events and rectangles for the event processors. 

---

# Passing off
You have two options for passing off this lab:

1. Come in person and pass off with the TAs. They'll have you walk through the workflow and explain your design decisions.
2. Package your code intelligbly and include a detailed writeup to explain the data and control flow, where the events are passed, and what design decisions you made. Email it to both TAs.

# Grading

- 25% &mdash; Guild properly distributes **rfq:delivery_ready** events to top three drivers
- 10% &mdash; Driver properly raises **rfq:bid_available** event to flower shop
- 20% &mdash; Flower shop properly raises **delivery:picked_up** event to Guild
- 10% &mdash; Driver notifies his system that the delivery has been completed
- 20% &mdash; Guild properly maintains driver rankings through an algorithm of your choice.
- 15% &mdash; Driver properly raises **delivery:complete** event to Guild and flower shop

