# Lab 6: Event-Based Programming

The purpose of this lab is to gain experience in programming event-based systems. 

# Reading

* [KRL Manual](http://developer.kynetx.com/display/docs/Manual)
* [Tips for Developers](http://developer.kynetx.com/display/docs/Tips+for+Developers)
* [Creating an Echo Server](http://developer.kynetx.com/display/docs/Creating+an+Echo+Server)

# Lab Notes

* The best way to use the KRL documentation is to search since you may not always appreciate how it's organized (or isn't).
* You will need to work through the [KRL Quickstart](http://developer.kynetx.com/display/docs/Quickstart) before beginning this lab.
* People often can't get their ruleset to run because it doesn't parse. Make sure you *always* parse your ruleset *before* checking it into whatever system you're using to store it (probably Github). 

# Part 1: Building a Simple Echo Service

The goal of this part of the lab is to understand how to write, debug, register, install, and operate KRL rulesets.

Do the following:

0. Using the recipe in [Creating an Echo Server](http://developer.kynetx.com/display/docs/Creating+an+Echo+Server) as a guide, write a ruleset named ```echo``` that contains two rules:

	1. Rule named ```hello``` that responds to a ```echo::hello``` event by returning a directive named ```say``` and the option ```something``` set to ```Hello World```

	2. Rule named ```message``` that responds to a ```echo:message``` event with an attribute ```input``` by returning a directive named ```say``` with the option ```something``` set to the value of the ```input``` attribute.

1. Parse your ruleset using one of the two methods from [Tips for Developers](http://developer.kynetx.com/display/docs/Tips+for+Developers).

2. Register your ruleset. 

3. Install the ruleset in your pico.

4. Use ```curl```, a program you write, or the [Sky Event Console](http://developer.kynetx.com/display/docs/Debugging+KRL+Rulesets#DebuggingKRLRulesets-eventconsoleUsingtheSkyEventConsole) to test your ruleset.

5. Write, register, and install a second ruleset named ```see_songs``` that contains a rule called ```songs``` that also responds to the ```echo:message``` event with an attribute ```input```. This rule should return a directive named ```sing``` with the option ```song``` set to the value of the ```input``` attribute.

6. Repeat the test you ran in (6) above. 

# Deliverables for Part 1

0. The source URLs for your rulesets
1. The RIDs for your rulesets
2. The ECI of a pico that your rulesets are installed in.
3. Answer the following questions:

## Questions for Part 1

0. What was the output of the test you ran in (5)?  How many directives were returned? How many rules do you think ran? 

1. What was the output of the test you ran in (7)?  How many directives were returned? How many rules do you think ran? 

2. How do you account for the difference? 

# Part 2:

The goal of this part of the lab is understand rule selection by attribute, explicit events, and rule chaining.

Do the following: 

1. Modify the ```songs``` rule you wrote in Part 1, step 6 so that it only selects when a ```msg_type``` attribute is equal to ```song```.

2. Test it by raising the ```echo:message``` event with and without the ```msg_type``` attribute set to ```song```.

3. Modify the ```songs``` rule from (1) to raise an explicit event with domain ```explicit``` and type ```sung``` and passes the input as the ```song``` attribute.

4. Write another rule in the same ruleset named ```find_hymn```  that selects on the ```explicit:sung``` event.  It should read the ```song``` attribute and if it contains the word ```god``` (in any case) raise another explicit event with domain ```explicit``` and domain ```found_hymn```.

5. Use ruleset logging and debugging tools to convince yourself that the rule from (4) works. 

# Deliverables for Part 2

0. The source URLs for your rulesets
1. The RIDs for your rulesets
2. The ECI of a pico that your rulesets are installed in.
3. Answer the following questions:

## Questions for Part 2

1. What did you observe in (2) above? How do you explain it?

2. Would you say that the new rule in (3) is an event intermediary? If so, what kind? Justify your answer.

3. How do your logs show that the rule in (4) works?  Pick out specific lines and explain them. 

# Part 3:

The goal of this part of the lab is to understand the [Event-Query API][event_query_api] and the use of entity variables and  modules.

Do the following:

1. Write a third ruleset called ```song_store```. This ruleset should have three rules:

   1.  A rule named ```collect_songs``` that looks for ```explicit:sung``` events and stores the ```song``` and a timestamp in an entity variable. The entity variable should contain all the songs that have been sung.
   2. A rule named ```collect_hymns``` that looks for ```explicit:found_hymn``` events and stores the hymn and a timestamp in a different entity variable that collects hymns.
   3. A rule named ```clear_songs``` that looks for a ```song:clear``` event and resets both of the entity variables from the rules in (1) and (2).

2. Add three  functions to the global block of the ```song_store``` ruleset:

	1.  A function called ```songs``` that returns the contents of the song entity variable.

	2. A called ```hymns```  that returns the contents of the hymn entity variable.

	3. A function called ```secular_music```  that returns all the songs in the song entity variable that aren't a hymn.

3. Add a [```provides``` pragma to the meta block][user_modules] of the ```song_store``` ruleset that lists the three functions from (2). Also add a [```sharing``` pragma to the meta block][sharing_pragma].

4. Test your song module by using events to notify the pico of songs sung and the [Sky Cloud API][skycloud] to retrieve them. You can use cURL, a program you write, or a browser app like the [Advanced REST Client][rest_client] to make calls to the functions.


# Deliverables for Part 3

1. The source URLs for your rulesets
2. The RIDs for your rulesets
3. The ECI of a pico that your rulesets are installed in.
4. A screenshot of the Installed Rule information from Devtools for the ruleset ```song_store``` showing your name, the sharing value, and the provided functions. 
5. Answer the following questions:

## Questions for Part 3

1. Explain how the rule ```collect_songs```  and the function ```songs``` illustrate an event-query API.

2. Explain your strategy for finding songs that aren't hymns in your ```secular_music``` function.

3. What happens if ```provides``` doesn't list the name of the ```songs``` function?

4. What happens if ```sharing``` is off?




[skycloud]: http://developer.kynetx.com/display/docs/Sky+Cloud+API

[event_query_api]: http://www.windley.com/archives/2013/12/pico_apis_events_and_queries.shtml

[rest_client]: https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US

[user_modules]: http://developer.kynetx.com/display/docs/User+Defined+Modules

[sharing_pragma]: http://developer.kynetx.com/display/docs/Meta+Section



<!--  LocalWords:  pragma
 -->
