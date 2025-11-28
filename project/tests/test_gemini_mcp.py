import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    # Define how to launch the server
    server_params = StdioServerParameters(
        command=sys.executable, # Use the current python interpreter
        args=["app/gemini_mcp.py"],
        env=os.environ # Pass current env (with GEMINI_API_KEY)
    )

    print("Starting Gemini MCP Client...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # 1. List available tools
                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print(f"\n✅ Connected! Found tools: {tool_names}")
                
                # 2. Call the 'ask_gemini' tool
                prompt = "Explain what the Model Context Protocol (MCP) is in one sentence."
                print(f"\n🚀 Sending prompt: '{prompt}'")
                
                result = await session.call_tool("ask_gemini", arguments={"prompt": prompt})
                
                # 3. Print the result
                if result.content and len(result.content) > 0:
                    print(f"\n🤖 Gemini Response:\n{result.content[0].text}")
                else:
                    print("\n⚠️ No content in response.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())
