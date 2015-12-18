# HTTP Methods, Headers, and Return Codes

The purpose of this lab is to increase your familiarity with HTTP.

# Reading

You may find these resources helpful:

- [HTTP Headers for Dummies](http://code.tutsplus.com/tutorials/http-headers-for-dummies--net-8039)
- [List of HTTP header fields](http://en.wikipedia.org/wiki/List_of_HTTP_header_fields)
- [List of HTTP status codes](http://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

# Lab Requirements

- Learn how to use a browser plugin that allows you to see details of HTTP requests and responses
- Write a Web script that users headers and status codes
- Use ```curl``` to exercise the Web script you wrote

# Part 0: HTTP Requests and Responses

For this part of the lab, explore the developer tools in your favorite browser.

0. Open www.byu.edu in your browser.  Where do you end up?
0. Using the browser tools, determine how many individual HTTP requests were made to create the page at ```http://home.byu.edu/home``` and the total time it took for those requests.
0. What is the name of main (primary) file for the page?  We'll refer to this as the root below. 
0. How long did it take to download the root? How long did the browser wait before it downloaded?
0. Does the root use caching? How can you tell?
0. What host did your browser report in the request header? What's the purpose of this header?
0. Were there any non-standard headers in the response?
0. Use ```curl``` to get ```http://www.byu.edu```. What is the status code? Why?

# Part 1: MIME-types

0. Create an HTML document in your Web server with the ```.byu``` extension.
0. Visit the URL of the document you created above in a browser. What is displayed? Why? 
0. Configure your Web server so that the file extension ```.byu``` maps to the ```text/html``` mime-type.
0. Revisit the document in the browser. Now what do you see? Why?

Hint: look at the response headers. 

# Part 2:  Web Script

For this part of the lab, you will create executables that are accessed through a Web server. I don't care what Web server you use. There are many you could choose from including Apache, NGINX, or lighttpd. You don't have to do this on an EC2 instance. You could use AWS Beanstalk. 

You're welcome to use the EC2 instance you create in [Lab0](https://github.com/windley/CS462-Event-Edition/blob/master/project/Lab0.md) or one of your own. You're can use any programming language you like.

0. Create a script that prints the headers in the request, any query string parameters, and the value of anything sent in the body of a POST. Use ```curl``` to show that it works.
0. Create a script that generates a redirect to one of several Websites based on the value of the query string. The mapping between the query string value and the URL to redirect to can be hard coded into the script. For example, a GET to ```http://my.domain.name/my_redirect_script?foo``` would  redirect to ```http://google.com``` if there was a mapping set up in the script between the keyword ```foo`` and Google's URL.

# Part 3: Versioning

0. Create a script that uses the Accept header to determine what is returns.
	- If the accept header is ```application/vnd.byu.cs462.v1+json``` return this JSON document
	
			{"version": "v1" }
			
	- If the accept header is ```application/vnd.byu.cs462.v2+json``` return this JSON document

			{"version": "v2" }
			
	- Ensure the Content-type header of the result is ```application/json```
	- Use ```curl``` to ensure your script functions correctly.


#Deliverable

Turn into the TA:

- Part 0: Your answers to the questions
- Part 1: In less that 150 words describe what happened. Explain why.
- Part 2: Describe your keyword mappings and provide the URL to your server
- Part 3: Provide the ```curl``` commands you used to exercise the versioning

The TA will expect to be able to test parts 2 and 3 using your provided URL and ```curl``` commands. 
