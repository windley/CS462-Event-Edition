
# Objectives

Introduce the purpose of transactions and demonstrate their use in an EJB-based n-tier implementation.


# Intro

- Story: [Someone Clue Delta in About Transactional Integrity](http://www.windley.com/archives/2011/05/someone_clue_delta_in_about_transactional_integrity.shtml)
- [Fandango - Buying Movie Tickets](http://www.fandango.com/)


## Summary

Consider the code from the ```TravelAgent``` bean in Monson-Haefel


    public TicketDO bookPassage(CreditCardDO card, double price) 
        throws IncompleteConversationalState {
        if (customer == null || cruise == null || cabin == null) {
            throw new IncompleteConversationalState();
        }
        try {
            Reservation reservation = 
                new Reservation(customer, cruise, cabin, price);
            entityManager.persist(reservation);

            this.processPayment.byCredit(customer, card, price);

            TicketDO ticket = new TicketDO(customer, cruise, cabin, price);

            return ticket;
        } catch(Exception e) {
            throw new EJBException(e);    
        }
    }

What happens if the ```processPayment``` method fails?  
  

A transaction is a sequence of operations that must all complete successfully, or must leave the system in the same state it was before the transaction began.  The classic example that demonstrates the behavior of a transaction is a bank account.  If we have a bank account system and we wish to transfer money from one account to another, we have to debit money from one account and credit to another.  Naturally, we'd like both operations to succeed, but if one fails, they must both fail.  Having one operation succeed and the other fail results in a bookkeeping error (and dissatisfied customers).  

Transactions should have four characteristics, remembered using the acronym [ACID](http://en.wikipedia.org/wiki/ACID):

* Atomic - a transaction executes completely or not at all
* Consistent - a transaction always maintains the integrity of the underlying data store (i.e. the data is in harmony with the real world that it models)
* Isolated - the operations in the transaction are not affected by operations outside the transaction
* Durable - the changed made by the operations in the transaction must persist in the face of system crashes

Consider what each of these means in terms of the example above.

## Isolation

Isolation is a special property that relies on characteristics of the data store.  There are three conditions we need to be aware of:

* Dirty read - a transaction reads uncommitted changes made by another transaction
* Repeatable read - data is guaranteed to look the same if read multiple times during the same transaction
* Phantom read - a transaction can see a record inserted by another transaction after the first transaction started 

Declarative transactions classify these as (moving from least restrictive to most restrictive):

* Read uncommitted - the transaction can read uncommitted data allowing dirty, non-repeatable, and phantom reads.
* Read committed - the transaction cannot read uncommitted data.  Dirty reads are prevented, but non-repeatable and phantom reads can still occur.
* Repeatable read - the transaction cannot change data that is being read by another transaction. Dirty and non-repeatable reads are prevented.  Phantom reads can still occur.
* Serializable - the transaction has exclusive read and write access to the data.  Dirty, non-repeatable, and phantom reads are prevented.

The [Wikipedia article on Isolation](http://en.wikipedia.org/wiki/Isolation_%28database_systems%29) has good examples of these. 

 Here's a table the shows how the isolation levels are releated to the isolation conditions above:

|                    | *Dirty*  | *Non-Repeatable* | *Phantom* |
|----------|-------|----------------|----------|
| *Read Uncommitted* |  Allowed | Allowed          | Allowed   |
| *Read Committed*   |  Allowed | Allowed          |           |
| *Repeatable Read*  |  Allowed |                  |           |
| *Serializable*     |          |                  |           |



As transaction become more and more restrictive, performance decreases.  Consistency and performance must be balanced.   Shared resource contention is a major cause of performance problems because it creates a bottleneck that you can't scale.  


## Transaction Context

![Transaction Context and Monitor](http://farm9.staticflickr.com/8526/8618584819_3dcb797006_o.png)

## Concepts

- Two Phase Commit Operation
    - Commit at end
    - Expense
- Systems that support transactions
    - EJB
	- .Net
- Ways of dealing with failure
	- TXNs and 2 Phase Commit
	- Retry
	- Waste
	- Compensating actions
- Trading off programmer time for performance


## References

Monson-Haefel, Richard Enterprise Java Beans, 5th Edition, O'Reilly, Chapter 16, pp. 357-406.

[ACID, Wikipedia](http://en.wikipedia.org/wiki/ACID)

[Isolation, Wikipedia.](http://en.wikipedia.org/wiki/Isolation_%28database_systems%29)

Gray, Jim (September 1981). ["The Transaction Concept: Virtues and Limitations" (PDF)](http://research.microsoft.com/~gray/papers/theTransactionConcept.pdf). Proceedings of the 7th International Conference on Very Large Databases. 19333 Vallco Parkway, Cupertino CA 95014: Tandem Computers. pp. 144–154. 
