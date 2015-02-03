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

0. Using the recipe in [Creating an Echo Server](http://developer.kynetx.com/display/docs/Creating+an+Echo+Server) as a guide, write a ruleset that contains two rules:

	1. Responds to a ```echo::hello``` event by returning a directive named ```say``` and the option ```something``` set to ```Hello World```

	2. Responds to a ```echo:message``` event with an attribute ```input``` by returning a directive named ```say``` with the option ```something``` set to the value of the ```input``` attribute.

1. Parse your ruleset using one of the two methods from [Tips for Developers](http://developer.kynetx.com/display/docs/Tips+for+Developers).

2. Register your ruleset. 

3. Install the ruleset in your pico.

4. Use ```curl```, a program you write, or the [Sky Event Console](http://developer.kynetx.com/display/docs/Debugging+KRL+Rulesets) to test your ruleset.

5. Write a second ruleset that contains a rule that also responds to the ```echo:message``` event with an attribute ```input```. This rule should return a directive named ```sing``` with the option ```song``` set to the value of the ```input``` attribute.

6. Repeat the test you ran in (5) above. 

# Deliverables for Part 1

0. The source for your ruleset
1. The RIDs for your rulesets
2. The ECI of a pico that your rulesets are installed in.
3. Answer the following questions:

## Questions for Part 1

0. What was the output of the test you ran in (5)?  How many directives were returned? How many rules do you think ran? 

1. What was the output of the test you ran in (7)?  How many directives were returned? How many rules do you think ran? 

2. How do you account for the difference? 

# Part 2:

Persistents and modules?


# Deliverables for Part 2


# Part 3:

Event dispatch


# Deliverables for Part 3


