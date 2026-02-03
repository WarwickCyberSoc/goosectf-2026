# MCP
## Step 1
Realise that the provided IP and port combo is an MCP server. This can be done by going to http://IP:PORT/mcp and seeing a response.

## Step 2
Use a MCP client / inspector to see all of the resources, prompts, and tools. 

Example inspector:
`npx @modelcontextprotocol/inspector --url http://IP:PORT/mcp`

## Step 3
Discover a tool named `find_flag` and run it. The response is the flag.
