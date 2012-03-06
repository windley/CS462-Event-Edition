# Lab 4: Event Intermediaries

**Objective:** Understand how intermediaries can be used in an event network. 

This lab introduces intermediaries in the form of a driver's guild that represents drivers, keeps track of driver performance, and distributes **rfq:delivery_ready** events.

Event intermediaries simplify some interactions in event networks and cut down on the number point-to-point subscriptions that players must maintain. 

The following diagram shows how this will work:

<a href="./Lab4-architecture.png"><img src="../../../raw/master/project/Lab4-architecture.png" alt="Lab 4 architecture" style="width: 90%" /></a>

---

# Driver's Guild

As you can see, the Driver's Guild is an organization that has it's own event network. 

- The guild subscribes to flower shops so that it sees **rfq:delivery_ready** events
- The drivers subscribe to the guild so that they see any **rfq:delivery_ready** events
- The guild will maintain a universal identifier for each driver

In addition, flower shops will signal a **delivery:picked_up** event to the guild when the delivery is picked up. The event will need to include the driver identifier.

Drivers will signal a **delivery:complete** event to the guild _and_ the flower shop when they have finished a delivery. 

The guild will maintain a ranking of delivery drivers based on performance. 

When the guild receives a **rfq:delivery_ready** event from a flower shop, it raises that event to the top three drivers based on performance (you can dummy up the data for testing purposes).  

*Exercise:* determine the event attributes for the new events introduced above. 

---

# Drivers

Your drivers will still maintain a database of flower shops and ESLs. When a driver sees a **rfq:deliver_ready** event from the guild, it will respond to the flower shop directly as it has in the past. The guild _does not_ intermediate the bid process.

The driver needs some way to notify his system when he has completed the actual delivery. You may use Twilio (as in Lab 3) or some other method.

---

# Implementation Notes

- You're free to determine how this ranking works. One possible solution is to base it on on-time performance for deliveries against a hypothetical best time. A production system would probably use a sophisticated service for this, but for our purposes, you can dummy up the ranking system and just update it with random performance rankings for each delivery. _Note:_ you **must** have a ranking system and update it, but it doesn't have to be "real."
- In Lab 3, you had direct subscriptions form the flowershops to the drivers. You will need to undo those subscriptions. Drivers should now *only* see **rfq:delivery_ready** events from the guild. 
- The universal driver identifier maintained by the guild will need to be an attribute on any event referencing a driver. 
- You may need transaction IDs or some other identifier to link events about a particular delivery. 

---

# Grading

- 30% &mdash; Guild properly distributes **rfq:delivery_ready** events to top three drivers
- 10% &mdash; Driver properly raises **rfq:bid_available** event to flower shop
- 20% &mdash; Flower shop properly raises **delivery:picked_up** event to guild
- 10% &mdash; Driver notifies his system that the delivery has been completed
- 30% &mdash; Driver properly raises **delivery:complete** event to guild and flower shop

