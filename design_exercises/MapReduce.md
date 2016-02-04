
# MapReduce Exercise

## Roles

* __master__--class instructor
* __grouper__--five students
* __mappers__--twenty two students who need a laptop, tablet or phone and a pencil or pen. Each mapper will have a number between 1 and 22.
* __reducers__--five students who need a pencil or pen

## Algorithm

1. Mapper N will
	1. Find the text for First Nephi Chapter N online
	2. Find all proper nouns in First Nephi Chapter N (do *not* count pronouns).
	3. Write each proper noun on an index card. One word per card. I.e. If Nephi occurs 20 times in your chapter, you will have 20 index cards with Nephi written on them. 
3. The Grouper will
	1. Get cards from the mappers
	2. Collate the cards into piles, one pile per proper noun. I.e. a pile for Nephi, a pile for Lehi, etc. 
	3. Distribute complete piles to reducers. All piles for a given noun go to same reducer. 
	4. No need to wait for all cards before distributing. 
4. Reducers are responsible or words in certain range (e.g. A-E, F-J, K-O, P-T, U-Z)
	1. Count the cards in each pile
	2. Produce one card with a list of the words and the count of each
	3. Give final card to the Master

## Questions

1. What is the role of the master?
2. What is the role of the mapper?
2. How does the mapper role differ from the role of the reducer? 
4. Why is there one grouper?
2. What work happened independently?
3. What work was dependent on other work?
5. How much longer would it take to count all the occurrences of every proper noun in the Book of Mormon, assuming you had enough workers to assign a chapter to each and increase the reducers proportionally?
6. How would you apply this method to
	1. Grouping words by length
	2. Find all verses that mention a specific word
	3. Count URL accesses for a large Web site with 1000s of servers
