
# Dealing with Failure

- Story: [Someone Clue Delta in About Transactional Integrity](http://www.windley.com/archives/2011/05/someone_clue_delta_in_about_transactional_integrity.shtml)
- [Transaction notes from Monson-Haefel](http://classes.windley.com/462/lectures/index.cgi?Transactions)
- [Fandango - Buying Movie Tickets](http://www.fandango.com/)
- [Starbucks Does Not Use Two-Phase Commit](http://eaipatterns.com/ramblings/18_starbucks.html)

## Concepts

- ACID
- Isolation
- Two Phase Commit Operation
    - Commit at end
    - Expense
- Systems that support transactions
    - EJB
	- .Net
- Journaled File Systems
- Distributed databases and eventual consistency
- Distributed consensus, Byzantine Generals problem
- Ways of dealing with failure
    - TXNs and 2 Phase Commit
	- Retry
	- Waste
	- Compensating actions
- Trading off programmer time for performance
