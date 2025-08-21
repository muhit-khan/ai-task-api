import asyncio
import json

# Mock MCP Server
async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")

    # Mock tool execution
    if message == "tool_call:get_weather":
        response = {"result": "Sunny"}
    else:
        response = {"error": "Unknown tool"}

    print(f"Send: {json.dumps(response)!r}")
    writer.write(json.dumps(response).encode())
    await writer.drain()

    print("Close the connection")
    writer.close()

async def run_mcp_server():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

# Mock MCP Client
async def run_mcp_client(tool_name: str):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    message = f"tool_call:{tool_name}"
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()
    return json.loads(data.decode())

# Example usage (can be run in a separate terminal)
if __name__ == "__main__":
    # To run the server: python -m app.mcp_integration
    # In another terminal, you can then run a client
    # import asyncio
    # from app.mcp_integration import run_mcp_client
    # asyncio.run(run_mcp_client("get_weather"))
    asyncio.run(run_mcp_server())