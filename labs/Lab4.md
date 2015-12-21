# Lab 4: Map Reduce

# Objectives

The purpose of this lab is to make you familiar with MapReduce as an example of a distributed system.

# Reading

- [Get Started: Count Words with Amazon EMR](http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-get-started-count-words.html)
- [Amazon EMR FAQs](http://aws.amazon.com/elasticmapreduce/faqs/)

# Requirements

- Run the sample Word Count application
- Run your own mapper and reducer scripts
- Explain what is happening

# Running the Word Count Sample 

0. Create a bucket in S3 using ```byu.<netID>``` as the name where ```<netID>``` is replaced by your net ID.
0. Follow the Amazon EMR instructions to run the sample ["word count"](http://aws.amazon.com/articles/2273) application. Be sure to use your bucket for output and logging. Also, please configure the job to auto-terminate.
0. Use the Monitor to watch your job run.  The status will change to "Waiting" after the job has completed.
0. Ensure the cluster terminates (i.e. the status should be "terminated") since these are large (and hence, expensive) servers.


# Run Your Own Mapper and Reducer Scripts

0. Repeat the example above, but use the [mapper.py](https://github.com/windley/CS462-Event-Edition/blob/master/code/mapreduce/mapper.py) and [reducer.py](https://github.com/windley/CS462-Event-Edition/blob/master/code/mapreduce/reducer.py) scripts available on Github. You're also free to rewrote these in some other EMR-supported language if you wish. Regardless, you should understand what each does.
0. Modify the scripts to sort the results. [This HowTo](https://wiki.python.org/moin/HowTo/Sorting) might come in handy if you're unfamiliar with Python. You can test your scripts by doing the following:

		cat file.txt | python mapper.py | python reducer.py

	The contents of file.txt shouldn't be long. Just long enough to know your scripts work. 

0. Note that the most frequent words are mostly uninteresting. These are called [stop words](https://en.wikipedia.org/wiki/Stop_words). Use this [list of English stop words](https://github.com/windley/CS462-Event-Edition/blob/master/code/mapreduce/stop-words) to modify the scripts once more so that they don't count stop words.
0. Now that your script sorts and removes stop words, run it on the text of a largish document such as one of the [books at Project Gutenberg](https://www.gutenberg.org/)

# Deliverables

0. Compare the time it took to run (1) above and to run it on the command line (2). Why does the command line seem so much faster?

1. Provide your code for (2) and (3) above (you may also supply links).

2. Discuss the results of (4). Why do you think you got the results you did? 
