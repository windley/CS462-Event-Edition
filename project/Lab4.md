# Lab 4: Event Intermediaries

**Objective:** Understand how intermediaries can be used in an event network. 

This lab introduces intermediaries in the form of a driver's guild that represents drivers, keeps track of driver performance, and distributes **rfq:deliver_ready** events.

Event intermediaries simplify some interactions in event networks and cut down on the number point-to-point subscriptions that players must maintain. 

The following diagram shows how this will work:

<a href="./Lab4-architecture.png"><img src="../../../raw/master/project/Lab4-architecture.png" alt="Lab 4 architecture" style="width: 90%" /></a>



- Flowershop now just has the guild ESL and signals it. 
- Guild knows about all drivers
- Drivers signal a **delivery_complete** event when they're done with the delivery. The guild ranks drivers in terms of their on-time performance.
- **rfq:delivery_ready** events are distributed to the top three drivers automatically as well as any that are within _n_ miles of the shop.  

