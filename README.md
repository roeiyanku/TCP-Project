# TCP Project – Reliable Data Transfer over TCP (Client–Server)

## Overview

This project implements a **client–server application in Python** that demonstrates **reliable data transfer concepts** such as **sliding window**, **ACK handling**, **timeouts**, and **retransmissions** on top of TCP sockets.

The goal is **educational**: to understand how transport-layer reliability mechanisms work by explicitly managing message flow, acknowledgments, and failures in user-space logic.

---

## Key Features

* Client–server architecture using **Python sockets**
* **Sliding window protocol** implementation
* Explicit **ACK tracking** and message sequencing
* **Timeout-based retransmissions**
* Multithreading for concurrent send/receive
* Configurable parameters (window size, timeout, message length)
* Can read configuration from **input or file**

---

## Project Structure

```
TCP-Project-master/
│
├── Client.py        # Client-side logic (send messages, receive ACKs)
├── Server.py        # Server-side logic (receive messages, send ACKs)
├── Common.py        # Shared protocol logic, constants, helpers
├── proto.py         # Protocol-related definitions / experiments
├── bla.txt          # Example input/config file
└── README.md        # Project documentation
```

---

## How It Works (High Level)

1. **Client** sends messages to the server in chunks.
2. Messages are sent according to a **window size**.
3. **Server** receives messages and sends back **ACKs**.
4. Client tracks ACKs:

   * If ACK received → advance window
   * If timeout expires → retransmit
5. Transfer completes when all messages are acknowledged.

This mimics core ideas behind TCP reliability while remaining transparent and debuggable.

---

## Sliding Window Example

If:

* Window size = 3
* Messages = M1, M2, M3, M4

Flow:

```
Send: M1 M2 M3
ACKs: A1 A2 A3
Send: M4
```

If M2 ACK is missing → only M2 is retransmitted.

---

## Running the Project

### 1️⃣ Start the Server

```bash
python Server.py
```

### 2️⃣ Start the Client

```bash
python Client.py
```

You will be prompted to enter:

* Message content (or file input)
* Window size
* Timeout value

---

## Configuration via File

You can provide parameters via a text file (example: `bla.txt`):

```
message: Hello World
window_size: 4
timeout: 2
```

This allows automated testing and reproducible runs.

---

## Technologies Used

* **Python 3**
* `socket` – networking
* `threading` – concurrent send/receive
* `time` – timeout handling

---

## Skills Demonstrated

* Network programming (TCP, sockets)
* Transport-layer concepts (ACKs, windows, retransmission)
* Multithreaded design
* Debugging distributed systems
* Clean separation of client/server/shared logic

---

## Why This Project Matters

This project demonstrates **real networking fundamentals** that are directly relevant to:

* Network Operating Systems (e.g. SONiC)
* Test automation for networking products
* Low-level system debugging
* Reliable communication protocols

---

## Possible Extensions

* Packet loss simulation
* Congestion control
* Selective vs cumulative ACKs
* Automated test suite (pytest)
* CI integration (GitHub Actions)

---

## Author

Roei Yanku
Computer Science B.Sc. Student

---

## License

Educational / academic use
