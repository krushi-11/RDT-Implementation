# Reliable Data Transfer (RDT) Protocol Implementation

A Python implementation of a reliable data transfer protocol using TCP sockets. This project demonstrates network programming concepts including error detection, packet loss handling, and reliable data transmission.

## 🌟 Overview

This implementation consists of three main components that work together to ensure reliable data transfer across an unreliable network:

- Sender (sender.py)
- Receiver (receiver.py)
- Utility Functions (util.py)

## 🚀 Features

- **Reliable Data Transfer**
  - Sequence numbering (0,1 alternating)
  - Acknowledgment system
  - Packet retransmission
  - Checksum verification

- **Error Handling**
  - Packet loss detection
  - Corruption detection
  - Timeout mechanism (5 seconds)
  - Automatic retransmission

- **Network Simulation**
  - Simulated packet loss (every 6th packet)
  - Simulated corruption (every 3rd packet)
  - Logging of received packets

## 🔧 Technical Details

### Packet Structure
```
[COMP][NETW][Checksum(2B)][Length+ACK+SEQ(2B)][Data]
```

### Components

#### 1. Sender (sender.py)
```python
Key Features:
- Sequence number management
- ACK processing
- Retransmission logic
- Three states:
  1. Original message
  2. Retransmission
  3. Socket timeout
```

#### 2. Receiver (receiver.py)
```python
Key Features:
- Packet verification
- ACK generation
- Error simulation
- Packet logging
```

#### 3. Utility Functions (util.py)
```python
Key Functions:
- create_checksum()
- verify_checksum()
- make_packet()
- extract_message()
- extract_seq_num()
```

## 📋 Prerequisites

- Python 3.x
- Basic understanding of:
  - Socket programming
  - Network protocols
  - Binary operations

## 💻 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. No additional dependencies required (uses standard Python libraries)

## 🎮 Usage

1. Start the receiver:
```bash
python receiver.py
```

2. Start the sender:
```bash
python sender.py
```

3. The receiver port is calculated as:
```python
receiver_port = 10100 + (4196840 % 500)
```

## 🔄 Protocol Flow

```plaintext
Sender                        Receiver
  |                             |
  |-------- Data Packet ------->|
  |                             | (Verify Checksum)
  |                             | (Process Packet)
  |<------- ACK Packet ---------|
  |                             |
```

## 📝 Implementation Details

### Error Detection
- 16-bit checksum calculation
- Binary operations for integrity verification
- Packet structure verification

### Retransmission Mechanism
- Timeout-based retransmission
- ACK-based reliability
- Sequence number verification

### Logging
- Received packets are logged in "received_pkt.txt"
- Packet details and status are printed to console

## 🧪 Testing Scenarios

1. Normal Operation
   - Successful packet transmission
   - Proper ACK reception

2. Error Scenarios
   - Every 6th packet: Simulated loss
   - Every 3rd packet: Simulated corruption
   - Timeout handling

## 🔍 Debugging

Common issues and solutions:
1. Packet Loss
   - Check timeout settings
   - Verify network connectivity

2. Corruption
   - Verify checksum calculation
   - Check packet structure

3. Connection Issues
   - Confirm port numbers
   - Check socket bindings

## 🛠️ Development

### Adding New Features
1. Extend error simulation
2. Add more packet types
3. Implement sliding window
4. Add congestion control

### Code Style
- Follow PEP 8 guidelines
- Document new functions
- Maintain error handling

## 📈 Performance Considerations

- Socket timeout set to 5 seconds
- Buffer size: 1024 bytes
- Maximum packet size considerations
- Checksum calculation efficiency

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 🔮 Future Improvements

1. Implementation Options:
   - Add sliding window protocol
   - Implement selective repeat
   - Add congestion control
   - Enhance error simulation

2. Performance Enhancements:
   - Optimize checksum calculation
   - Improve buffer management
   - Add compression

## ⚠️ Limitations

- Basic implementation for educational purposes
- No encryption
- Limited error types simulation
- Fixed sequence number (0,1)
- Single connection handling

## 📚 References

- Computer Networking: A Top-Down Approach
- Socket Programming in Python
- RFC Documents on Reliable Transfer
- TCP/IP Protocol Suite

## 👥 Authors

Krushikesh Thotange
