# Lab 5: Gossip Protocols

The purpose of this lab is to gain experience in peer-to-peer messaging using a gossip protocol by building a simple chat system. 

# Reading

- [Gossip Protocol](https://en.wikipedia.org/wiki/Gossip_protocol) - Wikipedia page is a nice intro
- [Gossip protocols for
large-scale distributed systems](http://sbrc2010.inf.ufrgs.br/resources/presentations/tutorial/tutorial-montresor.pdf) - tutorial slides
- [RFC 1036 - Standard for Interchange of USENET Messages](http://tools.ietf.org/html/rfc1036) - Old-style USENET news used a variant of a gossip protocol.
- [SWIM: Scalable Weakly-consistent Infection-style Process Group Membership
Protocol](http://www.cs.cornell.edu/~asdas/research/dsn02-SWIM.pdf)
- [Using Gossip Protocols For Failure Detection, Monitoring, Messaging And Other Good Things](http://highscalability.com/blog/2011/11/14/using-gossip-protocols-for-failure-detection-monitoring-mess.html)

# Lab Notes

* This lab builds upon the work you did in Lab 3. 

# Gossip Messages

The foundation of your gossip system will be messages that are exchanged between different instances of your software (or your friend's software if you implement it with interoperability in mind).

In most gossip protocol implementations, you'd pass messages over an unreliable protocol such as UDP. For simplicity we're going to use HTTP since you already know how to do this. This further simplifies the problem by using HTTP to fulfill the requirement the requirement to ensure messages were delivered. 

In a gossip-based messaging system, not every peer knows about all the others, so each peer must be able to forward messages it has received to other hosts who might not yet have received them, while ensuring that this forwarding does not cause infinite loops (e.g., A sends a message to B, which sends it back to A, which sends it back to B, etc.).

__This implies that each message will need a unique ID__ that can be used to keep track of chat messages.

Message IDs will consist of two parts (for reasons that will become clear in a minute):

0. A unique *origin ID*. Use a UUID. You'll need a UUID library for whatever language you're using. If no UUID library is available, you can make do with a long random number for this lab, although that would not be a good solution in a production system. 
1. A *sequence number* that distinguishes successive messages from a given origin. Each chat node will assign sequence numbers to chat messages consecutively starting with 0.

Message IDs made in this way make it easy for peers to compare notes on which messages from which other peers they have or have not yet received. For example, if A has seen messages originating from C up to sequence number 5, and compares notes with B who has seen C's messages only up to sequence number 3, then A knows that it should propagate C's messages 4 and 5 to B.

There are two kinds of messages:

* __Rumor Message:__ contains the text of the user message to be gossiped. The message is a JSON object containing the following fields:
    * ```Rumor```:&mdash;a JSON object with the following fields:
		* ```MessageID```&mdash;a string containing the unique ID for this message as described above. If you originated the message, it will be one you generated, otherwise you will use the message ID already in the message
		* ```Originator```&mdash;a string giving the name of the server (or user). This can be any text you would like to be displayed by the chat system 
		* ```Text```&mdash;a string containing the actual message.
	* ```EndPoint```&mdash;URL of the node propagating the rumor

	Here's an example:

            {"Rumor" : {"MessageID": "ABCD-1234-ABCD-1234-ABCD-1234" ,
                        "Originator": "Phil",
                        "Text": "Hello World!"
						},
			 "EndPoint": "https://example.com/gossip/13244"
            }

* __Want Message:__ summarizes the set of messages the sending peer has seen so far. The message is a JSON object containing the following fields:
    * ```Want```&mdash;a JSON object with the following fields:
		* ```<OriginID>```&mdash;the keys are the origin IDs that the sender knows about. The value associated with each key is a numeric value of the highest sequence value from this ```OriginID``` that the sender has seen. 
	* ```EndPoint```&mdash;URL of the node propagating the rumor

	Here's an example:

			{"Want": {"ABCD-1234-ABCD-1234-ABCD-125A": 3,
			          "ABCD-1234-ABCD-1234-ABCD-129B": 5,
		              "ABCD-1234-ABCD-1234-ABCD-123C": 10
		             } ,
			 "EndPoint": "https://example.com/gossip/asff3"
			}

# Propagating Rumors

Each node will run the following message propagation algorithm:

    while true {
	  q = getPeer(state)                    
      s = prepareMsg(state, q)       
      <url> = lookup(q)
      send (<url>, s)                 
      sleep n
    }

Each node will also provide an HTTP endpoint that responds to POST of valid messages in the following way:

	t = getMessage();
	if (  isRumor(t)  ) {
    	 store(t)
	} elsif ( isWant(t) ) {
	    work_queue = addWorkToQueue(t)
	    foreach w work_queue {
		  s = prepareMsg(state, w)
		  <url> = getUrl(w)
		  send(<url>, s)
          state = update(state, s)
		}
	}

The functions can be described as follows:

* ```getPeer()```&mdash;selects a neighbor from a list of peers. 
* ```prepareMessage()```&mdash;return a message to propagate to a specific neighbor
* ```update()```&mdash; update state of who has been send what. 
* ```send()```&mdash;make HTTP POST to send message

# Adding Messages

You will need a Web page for entering and displaying chat messages. A simple TEXTAREA for entering a messages followed by a list of messages received would be enough.

When the user submits a new message, you will need to add it to list of messages for this node and increment the sequence number. Note that you *don't* need to actually propagate the rumor. That will be done by the first algorithm shown above. 

# Deliverables 1

0. Implement the simple gossip scheme described above. Use the multi-tenancy you built in Lab 3 to allow it to work for multiple accounts from a single machine. Note that each account will need it's own URL for POSTing messages and the interaction between them should NOT assume they are on the same machine (even if they are). 
1. Test it by running three or four nodes of your own. 
2. Vary the value of ```n```, the length of time the propagation algorithm sleeps between iterations. What do you observe?
3. Try connecting your message system to another one built by someone else in the class. Make sure messages propagate. 
4. Answer the following questions:

## Questions

0. This lab uses a vector clock algorithm to create unique message IDs based on a sequence number.
   - could we replace the sequence number with a timestamp?
   - what are the advantages and disadvantages of such an approach?
1. Are the chat messages in order? Why or why not?  If not, what could you do to fix this? 
2. How did you avoid looping (sending messages back to someone who already has it)? Why was the unique ID helpful?
3. Why would a UUID be better than a long random number for creating the origin ID?
4. The propagation algorithm sleeps for ```n``` seconds between each iteration. What are the trade-offs between a low and high value for ```n```. 

# Adding Peers

Add a mechanism to keep track of a dynamically modifiable list of peers, each of which can have its own URL for POSTing messages.  This list will be the set of neighbors you pick from to gossip with. 

Your peer list should by default (on startup) include your nodes.  You should have two ways to add peers:

1. Use a web form  to add a peer dynamically while the program is running: e.g., a text-entry box that takes a name and URL.
2. When you receive a valid chat message that did not come from any of the currently registered peers, you should automatically add that peer, so that chat messages this node sends in the future will automatically go to this previously-unknown peer as well. This way you'll have to add a peer-to-peer link explicitly only in one direction; the other direction will get “learned” automatically.

The above functionality should give your application everything it needs, at least in theory, to operate “at large” over the Internet.

# Deliverables 2

0. Add dynamic peers to your gossip application
1. Test it by adding new nodes from both your own system and those of classmates.  Don't add all their nodes, just one.
2. Turn a node off and send some messages on the other nodes. Turn it back on. Did it catch up? 
3. Answer the following questions:

## Questions

0. Did new messages eventually end on all the nodes that were connected?
1. Were the messages displayed in the same order on each node? Why or why not?
2. Why does disconnecting a node from the network temporarily not result in gaps in the messages seen at that node?
3. Describe, in a  paragraph or two, how you could use the basic scheme implemented here to add failure detection to the system using a reachability table.
4. Describe how you would use the system built in this lab to disseminate Foursquare checkin data so that a group of people could know where the others are based on their Foursquare checkins. 



# Credit
This lab is very loosely based on ideas in [CPSC 426 Lab 1: Gossip Messaging](http://zoo.cs.yale.edu/classes/cs426/2014/lab/1-gossip)


