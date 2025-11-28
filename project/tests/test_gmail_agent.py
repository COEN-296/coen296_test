import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

async def run():
    # Define how to launch the server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["app/gemini_mcp.py"],
        env=os.environ
    )

    print("🚀 Starting Gmail Agent MCP Client...\n")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # 1. List available tools
                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print(f"✅ Connected! Available tools: {tool_names}\n")
                
                # 2. Test: Check emails
                print("📧 Test 1: Checking your emails...")
                result = await session.call_tool("agent_action", arguments={
                    "request": "List my last 5 emails"
                })
                
                if result.content and len(result.content) > 0:
                    print(f"\n📬 Result:\n{result.content[0].text}\n")
                else:
                    print("\n⚠️ No content in response.\n")
                
                # 3. Test: Send a test email to yourself
                print("\n📤 Test 2: Sending a test email to yourself...")
                gmail_user = os.getenv("GMAIL_USER")
                if gmail_user:
                    result = await session.call_tool("agent_action", arguments={
                        "request": f"Send an email to {gmail_user} with subject 'MCP Test' and body 'This is a test from the Gmail Agent!'"
                    })
                    
                    if result.content and len(result.content) > 0:
                        print(f"\n✉️ Result:\n{result.content[0].text}\n")
                    else:
                        print("\n⚠️ No content in response.\n")
                else:
                    print("⚠️ GMAIL_USER not set in .env, skipping send test.\n")
                
                print("✅ All tests complete!")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())
