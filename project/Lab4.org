# Lab 4: Event Intermediaries

**Objective:** Introduces intermediaries in the form of a driver's guild that represents drivers, keeps track of driver performance, and distributes **rfq:bid_needed** events.

- Flowershop now just has the guild ESL and signals it. 
- Guild knows about all drivers
- Drivers signal a **delivery_complete** event when they're done with the delivery. The guild ranks drivers in terms of their on-time performance.
- **rfq:bid_needed** events are distributed to the top three drivers automatically as well as any that are within _n_ miles of the shop.  

