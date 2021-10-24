# Importing the relevant libraries
import websockets
import asyncio

# Server data
PORT = 7890
print("Server listening on Port " + str(PORT))

# A set of connected ws clients
connected = set()

# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    # Store a copy of the connected client
    connected.add(websocket)
    # Handle incoming messages
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                # since this is a broadcast server, send the message to everyone except the sender
                if conn != websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        # if connection is closed, remove from the set of connections so that the broadcast does not happen to this client connection
        connected.remove(websocket)


# Start the server
start_server = websockets.serve(echo, "127.0.0.1", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
# server stays alive and does not stop working
asyncio.get_event_loop().run_forever()
