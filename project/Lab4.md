# Lab 4: Event Intermediaries

**Objective:** Understand how intermediaries can be used in an event network. 

This lab introduces intermediaries in the form of a driver's guild that represents drivers, keeps track of driver performance, and distributes **rfq:deliver_ready** events.

Event intermediaries simplify some interactions in event networks and cut down on the number point-to-point subscriptions that players must maintain. 

The following diagram shows how this will work:

<a href="./Lab4-architecture.png"><img src="../../../raw/master/project/Lab4-architecture.png" alt="Lab 4 architecture" style="width: 90%" /></a>

# Driver's Guild

As you can see, the Driver's Guild is an organization that has it's own event network. 
- The guild subscribes to flowershops so that it sees **rfq:delivery_ready** events.
- The drivers subscribe to the guild so that they see any **rfq:delivery_ready** events. 
- The guild will maintain a universal identifier for each driver

In addition, flowershops will signal a **delivery:picked-up** event to the guild when the delivery is picked up. The event will need to include the driver identifier.

Drivers will signal a **delivery:complete** event to the guild and the flowershop when they have finished a delivery. 

The guild will maintain a ranking of delivery drivers based on performance. 

When the guild receives a **rfq:delivery_ready** event from a flowershop it raises that event to the top three drivers based on performance (you can dummy up the data for testing purposes).  

*Exercise:* determine the event attributes for the new events introduced above. 

# Drivers

Your drivers will still maintain a database of flowershops and ESLs. When a driver sees a **rfq:deliver_ready** event from the guild, it will respond to the flowershop directly as it has in the past. The guild does not intermediate the bid process. 

# Implementation Notes

- You're free to determine how this ranking works, but it might be based on on-time performance for deliveries against a hypothetical best time. A production system would probably use a sophisticated service for this, but for our purposes, you can dummy up the ranking system and just update is with random performance rankings for each delivery. _Note:_ you need to have a ranking system and update it, but you don't need to make it "real."

# Passing Off
