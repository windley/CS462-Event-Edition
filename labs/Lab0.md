# Lab 0: AWS Introduction

# Objective

The purpose of this lab is to create a base server confirmation that will be used in future labs. You will modify an existing AMI (Amazon Machine Image) and configure it with a web server and a bootstrapping mechanism.

- Get an AWS instance running
- Set up a simple static Web page that displays your name, your custom AMI ID and User Data script.

# Lab Requirements 

- Boot an EC2 instance with an AMI that is "Free tier eligible"
- Install a web server with a basic configuration
- Serve a static web page that displays your name
- Create a custom AMI with your basic server configuration
- Add a bootstrapping procedure based on the User Data script supplied at launch

# Get Your AWS Educate Account

You will need to [sign up for an AWS Educate account](https://www.awseducate.com/Application). Even if you already have an AWS account, this will get you $100 of free credit. 

*Note: you are responsible for protecting your credentials. Their loss could result in substantial charges at Amazon which you will be responsible for covering. If your credentials are responsible for a breach, you may lose your Amazon privileges and have to find some other way to complete class requirements.*

*In particular, be sure that your AWS secret and password are __never__ hard coded into a file that will be stored in any public server. This is especially true of code you upload to Github.*

*Please remember to stop your instances when you are not using them.*

# Booting an AMI 

The AWS Management Console is the easiest way to control EC2 Instances. Amazon also provides command line tools, or you can use ElasticFox (a Firefox plugin).
- navigate to EC2 Dashboard, continue to Instances menu option.
- click Launch Instance.
- select Amazon Linux AMI.
- instance type "t2.micro"
- in configure make sure to change auto-assign Public IP to ENABLE, if you fail to do this, your instance will not have an ip address.
- you can create your own security group if you like or choose one that has already been made. if you create a new security group you will need to provide rules to allow traffic through for SSH and webpage viewing.

You will need to create a key pair that will allow you to login to the server after it has launched. If you use the AWS Management Console, this is part of the process to launch a new instance and is very simple to do.

for a more indepth guide go to http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-instance_linux.html


# Basic Web Server 

Use Apache to create a basic webserver. 

Install the necessary packages for Apache (or your server of choice). You can also install packages for the programming language you want to use in later labs if you wish.

Amazon guide for installing a LAMP web server has Apache install instruction if you need further help. http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-LAMP.html

# Simple index page

If accessed, the webserver should respond with a static page displaying your name.

The purpose of this page is simply to demonstrate that your web server is configured properly.

# Bootstrapping the Server 

The bootstrapping process allows you to start from a vanilla AMI or from your own custom AMI and automatically configure the server to install packages, run desired services, and download appropriate code.

The main piece of the process is the User Data script. This script is copied into the User Data field (or passed as a command line argument) when launching an instance. Launching an instance and starting an instance are not the same thing. It might install necessary packages, download your web app code from S3 or a Git repository.

One good solution is to have the script be very simple, downloading the full code for the server and then executing a more in-depth (and more easily updated) script that actually installs packages and copies the code to the proper locations.

Examples and explanations on User-scripts can be found on Amazon's website:
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html

# Creating and registering an AMI

After you are done modifying your custom AMI, you will need to persist the machine image and register it as an AMI. If you're using an EBS-backed instance (which is the default), this process is very easy. If you chose to use instance-store instead, talk to the TA for more detailed instructions on how to create the AMI.

With your instance running, right-click on it in the AWS Console and choose "Create Image (EBS AMI)". Name the image with your NetID and provide a description if you wish. Creating the image will take several minutes. When it finishes, you should see it in the AMIs section of the console.

Make note of your AMI ID, since you will need it for the passoff procedure.

# Implementation Notes 
You may find it useful to put your code in a Subversion or Git repository and have your bootstrap script copy the code from there to your server. This makes it very easy to update your server.

## Security Credentials
Everything in this lab can be done through the AWS Console online. In addition to the credentials supplied by the TA you will need to download to your computer is the keypair for logging into an EC2 instance.

This information will be useful if you choose to use AWS for the other labs in this class. Read through this information to become familiar with it, even though you may not need it.

### Keypair for launching EC2 instances
This is your personal private key used for launching and logging in to EC2 instances. You can create it the first time you launch an EC2 instance. When you do so, Amazon keeps a copy of the associated public key (which you will never see) and puts it in the appropriate place on every instance you launch. This allows you (and only you) to log in to your instances without needing to send a password.

You are the only person with this private key. If you lose it, you will have to create a new one. You will never use this key for anything except launching and logging in to EC2 instances.

### Access Key and Secret Access Key
These can be found in the Security Credentials page of the AWS Portal. They are used primarily for access to S3, whether via a scripting interface (e.g., boto) or via the command line (e.g., ec2-upload-bundle).

### X.509 Certificate and associated private key
The X.509 Certificate can be downloaded from the Security Credentials page, but the associated private key cannot. This is because the certificate is created once with an associated private key. Amazon does not keep a copy of that key, only the certificate.

The TA has a copy of this private key. Contact him to get it.

### Account number
This is found in the top right corner of the Security Credentials page. When you use it as a command-line argument for things like ec2-bundle-vol, you will need to remove the dashes.

### More information

You can log in to the AWS Portal with the username and password given in class.
Contact the TA if you need help.
You can find more information on the [AWS docs](http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys).

# Deliverables

- your instance should have a basic web server running, serving a web page with your name, AMI ID and a copy of your User Data script. 
- Email the TA with your instance ID and any URL exstenstion needed to veiw your webpage, please include any notes needed to view your page. Please place in the email subject line "Lab 0 passoff".
- The TA will verify your work by visiting your webpage and reviewing your custom AMI.




