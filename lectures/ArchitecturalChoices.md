
# Architectural Choices


##  Logical architecture

* Monolith or microservice
* Monolith: Two-tier, N-tier,
* API
* Mobile
* Web
* Events

## Physical architecture

* Load balancing
* Hosting method and platform
* Networks
* Caching
* Logging, monitoring, alerting

## Technology

* Languages
* External APIs
* Frameworks
* Server technology
* Database (e.g. SQL, NoSQL, normalized, de-normalized, consistency issues)
* Transport (e.g. HTTP, MQTT, overlay network, etc.)
* Ops automation
* i18n and l10n
* Serialization
* Transactions
* State (e.g. sessions, etc.)
* Asynchrony
* Naming and discovery


## Cross-cutting issues

* Coupling
* Security
* Scalability
* Reliability
* Deployment

## Other Factors

* Understand the load pattern of your application:
    * flat
    * spikey
    * smooth rolling changes
    * periodicity (daily, weekly, monthly, seasonal)

* Understand the user identity/session characteristics of your application. Lots of user data implies complicated business logic.

* What is the transactional nature of the site?

* Is your culture up to the architectural choices you're making?
