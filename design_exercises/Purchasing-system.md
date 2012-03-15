# Design exercise: Purchasing system

## Scenario
You will be designing a system to make online shopping easier. The user indicates to the system an intent to purchase an item. The system knows some of her preferences, vendor relationships, location, etc. It then submits a request for quote to several different merchants, along with relevant, anonymous information about the user. Each merchant then provides a personalized bid back to the system, based on the information in their own databases and the data provided in the RFQ. The user's system can then process those bids and notify the user about them according to her preferences.

## Events

Your solution must use events. Define the types of events you'll need, along with the attributes that must be passed along with them.

## User data

What kind of data does the system need to store for the user? How is that data anonymized and passed to the merchants such that it can't be tracked back to the user?

## Merchants

How does a merchant gain access to this platform to submit bids? How does a user select which merchants are allowed to make bids on her RFQs?

## Decision engine

Every user has different merchant preferences. For example, I may prefer to buy a product from Amazon over some other merchant because I like Amazon, even though it may cost a little more that way. The user must be able to indicate her preferences in some way. You may decide how that is implemented. Some possible schemes are weighting or prioritizing merchants.

## Notifying the user

- A user can specify how she wants to be notified of new bids (e.g., email, SMS, the next time she visits a web page, carrier pidgeon, snail mail, phone call, telegram, etc.). 
- It should be extensible so that third-party developers can create new ways of notifying the user. That is, you as the original system designer don't have to create the carrier pidgeon module yourself.
- A user may want to see only the winning bid or multiple bids.

# Do This

For each of the following steps, use whatever documentation technique that you think will communicate your plans.   Appoint one member of your group as the scribe and have that person record your architecture.  

- Describe the roles of the event network actors.  That is, what are the roles that users of the system will have?  What functionality is available to each of the roles? Which are the primary use cases.
- Describe the event model. What events does each party raise? What are their attributes. 
- Describe the data model.  What data needs to be stored and how is it structured?  
- Describe the user interface for the primary use cases.  
- What external APIs or services will you use?
- What internal API will you deliver? 

***Note:*** You don't have to do these in the order I have here.  You may want to do them some other way.  

# Deliverables

Put the following on a single poster page for display:

- Describe the primary roles.
- Diagram your data model
- Show the main events and their attributes
- Display the event hierarchy for your system

# Activity

The instructor will give this to you at the appropriate time.
