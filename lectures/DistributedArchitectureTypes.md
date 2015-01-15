# Types of Distributed Architectures

Distributed architectures comprise a system of processors of some sort that are interconnected to achieve some purpose. 

- Where is the processing done?
- How are the processors and other devices interconnected?
- Are they always connected the same way or does the connectivity change over time?
- What types of communication is used between nodes (e.g. RPC, Request-Response, Event, message, synchronous, asynchronous)
- Where is the information stored?
- What rules or standards are used?

Rather than thinking of the terms "distributed," "decentralized," and "distributed" as a linear arrangement, I like to picture them like so:

![System Type 2x2](https://raw.githubusercontent.com/windley/CS462-Event-Edition/master/lectures/system_type_2x2.png)

In this diagram, I use the terms "centralized" and "decentralized" to distinguish between systems that are made up of pieces that are all under the control of a single entity or not. I use the term "co-located" and "distributed" to indicate whether the functionality that is necessary to implement a system is co-located in a single process (at whatever level of abstraction is appropriate) or distributed among multiple processors. 

## Hierarchy vs Heterarchy

Heterarchy depends on

1. Collapse of functions. No hardwired distinctions in nodes

2. Freedom and ability to bypass. 

3. Decentralized and distributed resources


## Pipeline and Tree

Multiprocessor architectures

- Systolic
- MapReduce

Data centric


## Client Server

Processes have roles, either client or server

Layered applictions

- 2-tier
- N-tier and middleware
- Thin vs Thick client

Servers as clients

Vertically distributed

## Peer to Peer

No distinction between servers and clients. 

- Distributed objects (can be tightly (EJB) or loosely (pico) clustered)
- Event-bus
- Internet
- Overlay networks (SMTP, Web)

Horizontally distributed

## Network Principles are Universal

Video: [The surprising math of cities and corporations](http://www.ted.com/talks/geoffrey_west_the_surprising_math_of_cities_and_corporations) by [Geoffrey West](http://www.santafe.edu/about/people/profile/Geoffrey%20West)
