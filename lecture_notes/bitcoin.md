# Understanding Bitcoin and Distriuted 

Notes from [How the Bitcoin protocol actually works](http://www.michaelnielsen.org/ddi/how-the-bitcoin-protocol-actually-works/) by Michael Nielsen on December 6, 2013

## Forgery

Sign message "I Alice, am giving Bob one infocoin"

- Only Alice can create the message
- Others can duplicate it, but only after it's created

## Reuse

Put serial numbers in the messages

One solution is a central bank

- Bob contacts the bank
    - verifies infocoin with given serial number belongs to Alice
    - verifies Alice hasn't already spent it
    - bank keeps ledger showing transfer to Bob

Make everyone the bank

- Bob has a copy of a public ledger (e.g. blockchain) that he checks
    - Broadcasts a message
    - Everyone updates their copy of the ledger

## Double spending

Alice spends with Bob and Charlie

- as long as she times it right, Bob and Charlie will both think they're getting the infocoin
- Bob and Charlie should
    - check that Alice owns the coin using the blockchain
    - broadcast the transaction and ask others to verify
	- Some number of people need to validate


## Alice Takes Over

Alice can double spend as long as she has enough minions in the infocoin network

- Proof of work
    0. Make it artificially costly (computationally) to verify the transaction
	0. Reward verifiers for helping

Proof of work changes a "number of nodes on the network" problem to a "computational resource" problem

Calculate a hash with leading zeros for a "block" of transactions by varying a nonce. 

	h("Hello, world!0") = 
		1312af178c253f84028d480a6adc1e25e81caa44c749ec81976192e2ec934c64


	h("Hello, world!1") = 
		e9afc424b79e4f6ab42d99c81156d3a17228d6e1eef4139be78e948a9332a7d8

	h("Hello, world!4250") = 
		0000c3af42fc31103f1fdc0151fa747ff87349a4714df7cc52ea464e12dcd4e9

## No one wants to work for free

Validators need incentive to do the work

- give people infocoins for successfully validating a transaction
- call this "mining"

Bitcoin reward decays exponentially.

We can also include a transaction fee.


## Double Spending

Dishonest miners can potentially corrupt the validation process (proportional to computing power).

- Block *chain* orders transactions by linking a validation to the previously successful transaction
- Work on longest fork to avoid branching and ensure agreed-upon ordering of blocks.
- Transaction confirmed when 5 blocks follow it
- If Alice double spends with Bob and herself (alias), she has to have enough computational power to catch up with 5 blocks. < 10^-12 chance. 






