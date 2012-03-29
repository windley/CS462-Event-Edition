# Architectural choice exercise

For each of the following cases, describe and justify your choices in the following areas:

- Logical architecture
- Physical architecture
- Technology
- Infrastructure
- Cross-cutting issues
  - Security
  - Scalability
  - Reliability
  - Deployment

## Case 1: Reservations system

BYU Performing Arts want a new reservations system.

Requirements:

- Multiple venues
- Multiple events
- Customers browse events and selects specific seats, times, etc.
- Customer can add multiple events to cart system
- Events are held for a period of time between a customer selection and checkout
- Customer payment and reservation in a cryptographic package represent a "ticket"

## Case 2: Grad school paperwork

BYU Graduate School wants a workflow system for managing grad student study lists, advisory committees, etc.

Requirements:

- XML or JSON versions of documents
- Digital signatures for approvals by
  - Student
  - Advisor
  - Department
  - Grad School
- Completed, signed document is archives for legal purposes
- Ability to add new documents as necessary
- Users choose how they're notified that document awaits their approval
  - Email
  - Telephone message
  - SMS
  - RSS
- Flexible workflow by department (examples)
  - Department administrator determines which faculty (by NetID) are eligible to participate
  - Student picks adviser, adviser approves
  - Department assigns committee, student and adviser approve
- Only admitted grad students are allowed to participate

## Case 3: Photo site

Daily Universe wants a site where people can browse photos that have been in the Daily Universe by date, subject, keyword, and other metadata. Site allows people to submit photos for possible publication.

Additional requirements:

- Users can vote on favorite photos in a given time period
- Users can upload pictures
- Users can see the pictures they've uploaded
- Anonymous uploads are not allowed.
- All uploads from a non-NetID identifier are moderated
- The site includes a forum where registered users can discuss photos
- RSS feeds for photos from a user, highest rated, most recent, etc.

## Case 4: Social network for geeks

Your task is to design and deploy a question and answer site where developers and sysadmins can ask questions about specific technologies that are answered by other users. Users get points/reputation for their actions and priviledges on the site are determined by reputation. (i.e. this is StackOverflow)

## Case 5: Product recommendation service

You've teamed up with a genius who's created an engine that given a database of products can watch shopper actions and provide recommendations on what products go well together (i.e., recommendations). All interactions are done using an API. The problem is that it's temporally non-deterministic. You don't know if it will take 5ms or 5 minutes to return an answer for any given situation. Your job is to take that engine and build a system around it that can be sold to ecommerce sites.

