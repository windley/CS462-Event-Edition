
# APIs and Errors

Suppose you are designing an API to process class adds and drops for BYU. The basic form of the URL is

	  /courses/:cid/students/


 where ```:cid``` is the course ID. 

Doing an ```POST``` on this URL with a body that includes a student ID would add the student to the course.

Doing a ```DEL``` on this URL with a student ID as a suffix drops the student from the class like so

	/courses/:cid/students/:sid

where ```:sid``` is the student ID. 

In most cases, the system will return a ```200``` status code signifying that the action has been taken and all is well. But what happens if something goes wrong?

Consider the following scenarios:

1. A ```POST``` is made to add a class for which the student doesn't have the proper prerequisites. In this case, the add cannot happen. 

2. A ```DEL``` is made to drop a class that is a prerequisite for a course that the student has already registered for the next semester. In this case, the drop can happen only after the postrequisite course is dropped.

Design a response in keeping with the ideas in [How to GET a Cup of Coffee][get_coffee] for each of these error conditions that specifies:

1. The status code

2. Any headers

3. The response body

Ensure that the response body includes information about how the client can make forward progress where applicable. If you use relationship attributes (```rel```) be sure to define what they mean.  In contemplating this, ask yourself "what are the reasonable next states in this process?"




[get_coffee]: http://www.infoq.com/articles/webber-rest-workflow

