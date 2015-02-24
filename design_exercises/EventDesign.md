
# Event Design Exercise

The  [Event Expressions](http://developer.kynetx.com/display/docs/Event+Expressions) documentation describes event expressions in KRL. 

I've written a [post on the power of eventexes](http://www.windley.com/archives/2012/08/calculating_a_running_average_in_krl.shtml) in calculating a running average. 

The [slides I use in class](https://github.com/windley/CS462-Event-Edition/blob/master/lecture_notes/Event%20Expressions.pdf?raw=true) (PDF).


## Exercises

Use the lecture slides and the documentation linked above to answer the following exercises. 

Assume the following event streams:

0. Twitter stream (```tweet:received```) with attributes ```body``` and ```from```
0. Email IMAP account (```email:received```, ```email:sent```, ```email:forwarded```) with attributes, ```to```, ```from```, ```subj```, and ```body```
0. Stock price update stream (```stock:update```) with attribute ```ticker```, ```price```, ```change```, ```percent```, and ```name```)
0. Web pageview (```web:pageview```) with attributes ```url```, ```title```, and ```referer```.

Write event expressions that select the following:

0. Tweets containing the keyword "healthcare"
0. Emails with a body containing the words "BYU" and "football" in any order
0. Four tweets with the keyword "healthcare" within 4 hours
0. Tweet with keyword "healthcare" followed by an email with "healthcare" in the body or subject
0. More than five emails from the same person within a 20 minute period
0. Tweets that contain a stock-ticker symbol and the price of that same stock goes up by more than 2 percent within 10 minutes
0. User visits any two of Google, Yahoo!, MSNBC, CNN, or KSL.

Make up two scenarios involving a complex event expression and the preceding event streams. Write event expressions for them. 


