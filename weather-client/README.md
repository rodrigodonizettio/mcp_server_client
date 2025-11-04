# Overview

## How It Works

When you submit a query:

1. The client gets the list of available tools from the server
2. Your query is sent to Claude along with tool descriptions
3. Claude decides which tools (if any) to use
4. The client executes any requested tool calls through the server
5. Results are sent back to Claude
6. Claude provides a natural language response
7. The response is displayed to you
​
## Best practices

### Error Handling

- Always wrap tool calls in try-catch blocks
- Provide meaningful error messages
- Gracefully handle connection issues

### Resource Management

- Use AsyncExitStack for proper cleanup
- Close connections when done
- Handle server disconnections

### Security

- Store API keys securely in .env
- Validate server responses
- Be cautious with tool permissions
- Prompt for user confirmation on sensitive operations

#### Clients SHOULD

- Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration
- Validate tool results before passing to LLM
- Implement timeouts for tool calls
- Log tool usage for audit purposes

### Tool Names
- Tool names can be validated according to the __format specified below__:
    - Tool names SHOULD be between 1 and 128 characters in length (inclusive).
    - Tool names SHOULD be considered case-sensitive.
    - The following SHOULD be the only allowed characters: uppercase and lowercase ASCII letters (A-Z, a-z), digits (0-9), underscore (_), dash (-), and dot (.)
    - Tool names SHOULD NOT contain spaces, commas, or other special characters.
    - Tool names SHOULD be unique within a server.
    - Example valid tool names: ```getUser ; DATA_EXPORT_v2 ; admin.tools.list```
- If a tool name conforms to the specified format, it should not fail validation by an MCP client