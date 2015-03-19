
# Paxos

- What is consensus?

- Perhaps most important algorithm in Distributed Computing

# Paxos Problem

The safety requirements for consensus are:

- __Termination:__ Only a value that has been proposed may be chosen,
- __Agreement:__ Only a single value is chosen, and
- __Integrity:__ A process never learns that a value has been chosen unless it actually has been.

Liveness requirements:

- ensure that some proposed value is eventually chosen
- if a value has been chosen, then a process can eventually learn the value

# Assumptions

Model:

- agents can communicate with one another by sending messages
- agents operate at arbitrary speed, may fail by stopping, and may restart
- agents have some persistent storage. (Since all agents may fail after a value is chosen and then restart, a solution is impossible unless some information can be remembered by an agent that has failed and restarted.)
- messages can take arbitrarily long to be delivered, can be duplicated, and can be lost, but they are not corrupted.

Note that there is no "Byzantine" failure.


# Roles

- proposer --- propose values
- acceptor --- choose among proposed values
- learner --- learn a chosen value

In Paxos all nodes play all three roles in different phases of the algorithm. 

# Choosing a Value: Initial Solution

Requirement:

__P1:__ An acceptor must accept the first proposal that it receives

Problem:

Several values could be proposed by different proposers at about the
same time, leading to a situation in which every acceptor has
accepted a value, but no single value is accepted by a majority of
them.

![Initial Attempt: What happens if an acceptor goes offline?][fig:init]



# Choosing a Value: Initial Solution

The Fix:


__P2:__ If a proposal with value v is chosen, then every higher-numbered proposal that is chosen has value v.

- Allows restart


# Properties of Initial Solution

- P1 ensures obstruction-free process and validity
- P2 ensures agreement
__Problem:__ Can nodes going offline cause nodes to chose another proposal?

![What happens if p_1 and p_2 go offline after red is chosen?][fig:numbers]




# Implementing P2: Key idea

Important: a proposal can only be accepted if it is issued

So

__P2b:__ If a proposal with value v is chosen, then every higher-numbered proposal that is issued has value v.

P2b => P2

But all processes may not be online, so

__P2c:__ For any v and n, if a proposal with value v and number n is issued,
then there is a set S consisting of a majority of acceptors such that
either

1. no acceptor in S has accepted any proposal numbered less than n, or
2. v is the value of the highest-numbered proposal among all proposals numbered less than n accepted by the acceptors in S.

P2c => P2b => P2

![Disallow proposals after a choice is made][fig:limit]




# Implementing P2:

## Algorithm, Preparation Step

1. A proposer selects a proposal number n and sends a prepare  request with number n to a majority of acceptors.
 
2.  If an acceptor receives a prepare request with number n greater than that of any prepare request to which it has already responded, then it responds to the request with a *promise* not to accept any more proposals numbered less than n and with the highest-numbered proposal (if any) that it has accepted.

## Algorithm, Accept Step

1. If the proposer receives a response to its prepare requests (numbered n) from a majority of acceptors, then it sends an accept request to each of those acceptors for a proposal numbered n with a value v, where v is the value of the highest-numbered proposal among the responses, or is any value if the responses reported no proposals.

2. If an acceptor receives an accept request for a proposal numbered n, it accepts the proposal unless it has already responded to a prepare request having a number greater than n.

## Learning the Chosen Value

A distinguished learner tells all the other learners of the new value.

Since all nodes play all roles, this can be any node that knows the value.


## Distinguished Proposer


__Problem:__ Two proposers can trade off making conflicting proposals with ever higher numbers without one being accepted

__Solution:__ Use a distinguished proposer

We avoid centralization by providing a fair algorithm for electing the distinguished node regardless of failure. Fair election is typically done by giving nodes an ordinal number and accepts the highest numbered node that has been heard from in a given amount of time (e.g. last 5 milliseconds).


# References

I made use of the following in developing these notes:

[Paxos Made Simple][pms]

[Lecture 10. Unit 2 Paxos-Algorithm by Seif Haridi][sh2]

[pms]: http://cseweb.ucsd.edu/classes/sp11/cse223b/papers/paxos-simple.pdf

[sh2]: https://www.youtube.com/watch?v=5scBtoyz8HU


[fig:init]: figures/paxos.png/InitialAttempt.png

[fig:numbers]: figures/paxos.png/BallotNumbers.png

[fig:limit]: figures/paxos.png/LimitProposals.png

