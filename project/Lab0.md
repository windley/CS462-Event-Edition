# Lab 0:

The purpose of this lab is to create a base server confirmation that will be used in future labs. You will modify an existing AMI (Amazon Machine Image) and configure it with a web server and a bootstrapping mechanism.

- Get an AWS instance running
- Set up a simple static Web page that displays your name

# Lab Requirements 

- Boot an EC2 instance based on an Ubuntu 11.10 AMI (ami-bf62a9d6)
- Add a bootstrapping procedure based on the User Data script supplied at launch
- Install a web server with a basic configuration
- Serve a static web page that displays your name
- Create a custom AMI with your basic server configuration

# Passoff Procedure 

- Email the TA (cs462ta@gmail.com) with this information, provide the AMI ID of your custom AMI, the User Data (bootstrapping) script you wish to use, and your full name. Please place in the email subject line "Lab 0 passoff".

# Booting an AMI 

The AWS Management Console is the easiest way to control EC2 Instances. Amazon also provides command line tools, or you can use ElasticFox (a Firefox plugin).

You will need to create a key pair that will allow you to login to the server after it has launched. If you use the AWS Management Console, this is part of the process to launch a new instance and is very simple to do.

Find your AMI in the provided list and launch it. If you are using the standard Ubuntu Server 11.10 AMI, you can follow this link: <https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-bf62a9d6>.

# Basic Web Server 

Use Apache to create a basic webserver.

Install the necessary packages for Apache (or your server of choice). You can also install packages for the programming language you want to use in later labs if you wish.

# Simple index page

If accessed, the webserver should respond with a static page displaying your name.

The purpose of this page is simply to demonstrate that your web server is configured properly.

# Bootstrapping the Server 

The bootstrapping process allows you to start from a vanilla AMI or from your own custom AMI and automatically configure the server to install packages, run desired services, and download appropriate code.

The main piece of the process is the User Data script. This script is copied into the User Data field (or passed as a command line argument) when launching an instance. It might install necessary packages, download your web app code from S3 or a Git repository.

One good solution is to have the script be very simple, downloading the full code for the server and then executing a more in-depth (and more easily updated) script that actually installs packages and copies the code to the proper locations.

# Creating and registering an AMI

After you are done modifying your custom AMI, you will need to persist the machine image and register it as an AMI. If you're using an EBS-backed instance (which is the default), this process is very easy. If you chose to use instance-store instead, talk to the TA for more detailed instructions on how to create the AMI.

With your instance running, right-click on it in the AWS Console and choose "Create Image (EBS AMI)". Name the image with your NetID and provide a description if you wish. Creating the image will take several minutes. When it finishes, you should see it in the AMIs section of the console.

Make note of your AMI ID, since you will need it for the passoff procedure.

# Notes 
You may find it useful to put your code in a Subversion or Git repository and have your bootstrap script copy the code from there to your server. This makes it very easy to update your server.

## Security Credentials
Everything in this lab can be done through the AWS Console online. The only key you will need to download to your computer is the keypair for logging into an EC2 instance.

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

