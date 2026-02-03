from fastmcp import FastMCP
import random

mcp = FastMCP('goose')

@mcp.tool()
async def find_flag() -> str:
    return 'GooseCTF{y0u_mus1_b3_glad05}'

# Tools to hide flag tool
@mcp.tool()
async def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

@mcp.tool()
async def reverse_string(text: str) -> str:
    return text[::-1]

@mcp.tool()
async def get_random_number(min_val: int = 0, max_val: int = 100) -> int:
    return random.randint(min_val, max_val)

@mcp.tool()
async def count_vowels(text: str) -> int:
    return sum(1 for char in text.lower() if char in 'aeiou')

if __name__ == '__main__':
    mcp.run(transport='http', host='0.0.0.0', port=8000)