# APIs and OAuth

# Objective

Build a web application on your AWS server that does the following:

- Has multiple accounts with a profile page for each user. This includes the ability to create accounts, log in, and log out.
- Support SSL requests.
- Allows a user to authorize the application to access their account on Foursquare using OAuth.
- Retrieves user checkin information from Foursquare.
- When the user is logged in and is viewing their own profile, display their detailed checkin data (venue and a few other fields of your choice).
- When the user is logged out and is viewing their own profile, display only the most recent checkin.
- Whether the user is logged in or out and is viewing the profile of any other user on the system, display only the most recent checkin.

# Foursquare API

The Foursquare API documentation is here:
- [OAuth](https://developer.foursquare.com/overview/auth)
- [API endpoints](https://developer.foursquare.com/docs/)

# Implementation notes

You may use any language (e.g., Ruby, Python, PHP, C#, Racket, Perl, or assembly), framework, or libraries you wish. You need not learn KRL for this lab.

All requests to the Foursquare API must go over HTTPS. Make sure your server supports it for incoming requests, and ensure that you make all requests that way.

You will only be requesting data from Foursquare, not posting any data.

Foursquare uses OAuth 2, not 1.0a. Make sure your library (if you use one) supports that version of the protocol.

If you use EC2, the public DNS of your EC2 instance will change every time the machine is launched or started. That means you will need to update the application (consumer) details on Foursquare every time the server's name changes.

While your Web application _must_ support multiple accounts, it doesn't have to provide authentication for those accounts. 

You may wish to include a list of all registered users on the landing page of your app with links to view their profiles.

You will probably want to have your server persist accounts so that you can start and stop it without having to recreate everything. A simple way to do that is to write the account data as JSON into a file and then read and decode that file when you start up. You can easily flush the data from memory to the file on any change to the data. For what we're doing this will work fine. If you like, you're also welcome to use a simple database like Berkeley DB or a hosted database like the one from MongoLab.com. 

# Grading
- 33% &mdash; Multiple accounts supported
- 33% &mdash; Foursquare OAuth properly executed
- 34% &mdash; Foursquare checkins properly retrieved and displayed

You will need to demonstrate (By showing in person or email the Ip and aim # (if it's running on the Amazon cloud).) that multiple Foursquare accounts can use OAuth to authorize your Web application and that your application can correctly associate Foursquare checkin data from a particular user with that user's account on your Web application. Feel free to have other class members link their Foursquare accounts to your Web application to test this. 

