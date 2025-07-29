from agents import function_tool

@function_tool
def set_thermostat(temp: float, room: str = "Living Room") -> str:
    """Sets the thermostat to a specific temperature in a given room."""
    print(f">> ACTION >> Thermostat in {room} set to {temp}°C.")
    return f"SUCCESS!. The thermostat in {room} has been set to {temp}°C."

@function_tool
def turn_light_on(room: str, brightness: int = 100) -> str:
    """Turns on the light in a given room with a given brightness (1-100)."""
    print(f">> ACTION >> Light in {room} turned on with brightness {brightness}.")
    return f"SUCCESS!. The light in {room} has been turned on with brightness {brightness}."

@function_tool
def play_music(artist: str, song: str) -> str:
    """Plays a song by specific artist."""
    print(f">> ACTION >> Playing {song} by {artist}.")
    return f"SUCCESS!. {song} by {artist} is now playing."
