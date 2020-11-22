DNS Cache Poisoning Attack Demo
===============================

This project is to investigate and reproduce the DNS Cache Poisoning Attack within an isolated network environment using docker. The demo shows an adversary to spoof the DNS answer of google.com and direct to the adversary's malicious IP address.

## Quickstart

### Prerequisities

You will need Docker and Docker Compose installed for this project.

### Build

```bash
docker-compose build
docker-compose up
```
Upon running, the DNS resolver and upstream DNS server will start listening on port 53.

### Attack

#### 1. Into the container `attacker`

```bash
docker exec -it attacker bash
```

#### 2. Launch the attack script

```bash
python attack.py google.com 10.0.0.4
```

#### 3. Impact

![](/screenshots/1.png)

As the output of the container `dns` shows, a fake DNS record has been successfully written into cache. It can be verified by using dig in the victim's container.

First get into `victim`'s container:

```bash
docker exec -it victim bash
```

In the container:

```bash
dig google.com
```

![](/screenshots/2.png)

It shows that in the answer section, the record is pointing to the adversary's IP address (10.0.0.4).

## Debriefing

### Project Architecture

Four containers are used in this project:\
`DNS` (`10.0.0.2`): A vulnerable DNS resolver\
`Victim` (`10.0.0.3`): A victim host for proving the attack\
`Attacker` (`10.0.0.4`): The adversary who will launch the attack\
`Upstream DNS` (`10.0.0.5`): Plays the role of an upstream DNS server

### DNS Cache Server (`10.0.0.2`)

This is a simple DNS resolver developed to fully examine the attack process. It first looks at the cache stored and returns the cache if there is. Otherwise, it will forward the request to the upstream DNS server, waiting for responses.

As the objective of this project is only to investigate the attack itself, the Query ID (QID) for requesting is always set to range from 10000 to 10050, and the source port is fixed to 22222 to avoid launching a birthday attack, which is not the goal of this project.

Once received the response, it will validate if two QIDs match and then send the answer to the client.

### Upstream DNS (`10.0.0.5`)

A local authoritative DNS is set up to take the place of upstream DNS servers to always respond DNS requests with IP `1.2.3.4`

### Attacker (`10.0.0.4`)

The adversary first sends a DNS query to the DNS cache server (`10.0.0.2`), so the server will send a DNS request to the upstream server and begin accepting responses. Then it sends DNS answers trying all possible QID from the destination impersonating the upstream server (`10.0.0.5`) to the cache server (`10.0.0.2`).

An attack script (`/attacker/attack.py`) is thereby created.

#### Usage:
```bash
python attack.py [target domain] [spoofed IP]
```

## License

This was initially developed for CS 4404 Network Security B20 as a part of Mission 2 for Team 13 and is licensed under the [MIT License](LICENSE). However, you may NOT directly use this repository if you are taking the same course as a student as per Academic Integrity Policy.
