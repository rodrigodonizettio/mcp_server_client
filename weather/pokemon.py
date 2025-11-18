from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


POKEMON_API_BASE = "https://pokeapi.co/api/v2/"


async def make_pokemon_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Pokemon API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making GET HTTP request to {url}: {e}")
            return None


def format_pokemon(pokemon: dict) -> str:
    """Format JSON object from PokemonAPI"""
    if not isinstance(pokemon, dict):
        return "Invalid Data"

    name = pokemon.get("name", "unknown").capitalize()
    pid = pokemon.get("id", "N/A")
    base_exp = pokemon.get("base_experience", "N/A")
    height = pokemon.get("height", "N/A")
    weight = pokemon.get("weight", "N/A")

    types = ", ".join(
        t.get("type", {}).get("name", "unknown") for t in pokemon.get("types", [])
    ) or "Unknown"

    abilities = []
    for ability in pokemon.get("abilities", []):
        aname = ability.get("ability", {}).get("name", "unknown")
        hidden = ability.get("is_hidden", False)
        abilities.append(f"{aname}{' (hidden)' if hidden else ''}")
    abilities_str = ", ".join(abilities) or "None"

    stats_lines = []
    for stat in pokemon.get("stats", []):
        stat_name = stat.get("stat", {}).get("name", "unknown")
        base = stat.get("base_stat", "N/A")
        stats_lines.append(f"{stat_name}: {base}")
    stats_str = "\n            ".join(stats_lines) if stats_lines else "None"

    sprites = pokemon.get("sprites", {}) or {}
    sprite_url = (
        sprites.get("other", {})
        .get("official-artwork", {})
        .get("front_default")
        or sprites.get("front_default")
        or "No image available"
    )

    moves = [move.get("move", {}).get("name", "unknown") for move in pokemon.get("moves", [])]
    moves_str = ", ".join(moves) if moves else "None"

    held = [item.get("item", {}).get("name", "unknown") for item in pokemon.get("held_items", [])]
    held_str = ", ".join(held) or "None"

    return f"""
        Name: {name} (ID: {pid})
        Base experience: {base_exp}
        Height: {height}
        Weight: {weight}
        Types: {types}
        Abilities: {abilities_str}
        Held items: {held_str}
        Sprites: {sprite_url}

        Stats:
            {stats_str}

        Example moves: {moves_str}
    """


"""The FastMCP class uses Python type hints and docstrings to automatically generate tool definitions, 
making it easy to create and maintain MCP tools.
"""
mcp = FastMCP("pokemon")


@mcp.tool()
async def get_abilities(pokemon_name: str) -> str:
    """Get pokemon abilities based in pokemon name.

    Args:
        pokemon_name: The pokemon name (e.g. ditto, pikachu)
    """
    url = f"{POKEMON_API_BASE}/pokemon/{pokemon_name}"
    data = await make_pokemon_request(url)

    if not data or "abilities" not in data:
        return "Unable to fetch abilities or no abilities found."

    if not data["abilities"]:
        return "No abilities for this pokemon."

    abilities = []
    for ability in format_pokemon(data)["abilities"]:
        abilities.append(ability["ability"]["name"])
    return "\n---\n".join(abilities)


@mcp.tool()
async def get_moves(pokemon_name: str) -> str:
    """Get pokemon moves based in pokemon name.

    Args:
        pokemon_name: The pokemon name (e.g. ditto, pikachu)
    """
    url = f"{POKEMON_API_BASE}/pokemon/{pokemon_name}"
    data = await make_pokemon_request(url)

    if not data or "moves" not in data:
        return "Unable to fetch moves or no moves found."

    if not data["moves"]:
        return "No moves for this pokemon."

    moves = []
    for move in format_pokemon(data)["moves"]:
        moves.append(move["move"]["name"])
    return "\n---\n".join(moves)


def main():
    print('Initializing MCP Server...')
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()