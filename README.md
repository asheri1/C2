
# C2 Command and Control (C&C) Application

This project implements a C2 (Command and Control) system designed for managing and dispatching commands to connected agents. The system includes two components: the **Server** (C&C Controller) and the **Client** (Agent).

## Features

### Server
- **Client Management**: Maintains a list of connected agents, managing their liveness via keep-alive messages.
- **Command Dispatching**: Allows sending commands to individual clients or broadcasting to all clients.
- **CLI Interface**: Provides a command-line interface for operators to:
  - Send commands to clients.
  - Remove/kill clients.
  - Display command execution results.
- **Status Monitoring**: Displays real-time status of connected clients and their command execution processes.
- **Plug-n-Play Commands**: Supports additional command types via plug-and-play capabilities, allowing easy extension of commands.

### Client
- **Keep-Alive Messages**: Sends periodic keep-alive messages to the server.
- **Command Execution**: Receives, processes, and executes commands sent by the server.
- **Command Structure**:
  - Command payload (saved as a file and executed).
  - Command type, unique identifier, and arguments.
- **Command Status Reporting**: Reports command execution status (Received, Initialized, Running, Finished, Error) back to the server.
- **Result Transmission**: Sends results in base64 encoding or error messages, along with the command identifier.
- **Multithreading**: Manages commands in a queue and executes each in a separate thread.
- **File Management**: Deletes command payload files after execution and result transmission.

## Installation

1. Install Python.

2. Clone the repository:
   ```bash
   git clone https://github.com/asheri1/C2.git
   cd C2
   ```

## Usage

### Server:
Start the server (with the CLI):
```bash
cd server_side
python3 CLI.py
```

Monitor and manage agents through the CLI interface.

### Client:
Start the client:
```bash
cd client_side
python3 client.py 
```

The client will connect to the server and listen for commands.

## Configuration

The client configuration file should include:
- Server IP and Port.
- Keep-alive interval.
- Command execution directory.

The server configuration includes refresh intervals for status monitoring and CLI options.

## Logging and Error Handling
Both server and client handle exceptions and log their operations for debugging and monitoring purposes.
