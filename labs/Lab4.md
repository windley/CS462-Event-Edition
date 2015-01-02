# Lab 4: Map Reduce

The purpose of this lab is to make you familiar with MapReduce as an example of a distributed system.

# Reading

- [Get Started: Count Words with Amazon EMR](http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-get-started-count-words.html)

# Requirements

- Run the sample Word Count application
- Run your own mapper and reducer scripts
- Explain what is happening

# Running the Word Count Sample 

0. Create a bucket in S3 using ```byu.<netID>``` as the name where ```<netID>``` is replaced by your net ID.
0. Follow the Amazon EMR instructions to run the sample "word count" application. Be sure to use your bucket for output and logging. Also, please configure the job to auto-terminate.
0. Use the Monitor to watch your job run.  The status will change to "Waiting" after the job has completed.
0. Ensure the cluster terminates (i.e. the status should be "terminated") since these are large (and hence, expensive) servers.


# Run Your Own Mapper and Reducer Scripts

0. Repeat the example above, but use the mapper.py and reducer.py scripts available on Github. You're also free to rewrote these in some other EMR-supported language if you wish. Regardless, you should understand what each does.
0. Modify the scripts to sort the results. [This HowTo](https://wiki.python.org/moin/HowTo/Sorting) might come in handy if you're unfamiliar with Python. 
