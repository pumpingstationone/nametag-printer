import keyboard
from printer import print_name


def lookup_rfid(rfid_tag):  # Placeholder
    """Lookup the name corresponding to the RFID tag."""
    rfid_to_name = {
        "1234567890": "John Doe",
        "0987654321": "Jane Smith",

        # Actual RFID used for testing:
        "0006765820": "Pumping Station: One",
    }
    return rfid_to_name.get(rfid_tag)


def listen_for_rfid():
    """Listen for RFID inputs via the keyboard."""
    print("Listening for RFID scans...")
    buffer = ""
    while True:
        event = keyboard.read_event()
        if event.event_type == "down":  # Only process key press events
            char = event.name
            if char == "enter":  # Linebreak indicates end of RFID input
                if len(buffer) == 10 and buffer.isdigit():
                    print(f"RFID Tag Detected: {buffer}")
                    name = lookup_rfid(buffer)
                    if name:
                        print(f"Matched Name: {name}")
                        print_name(name)
                buffer = ""  # Clear the buffer after processing
            elif char.isdigit():  # Append digits to the buffer
                buffer += char
                buffer = buffer[-10:]
                print(f"Buffer: {buffer}")


if __name__ == "__main__":
    listen_for_rfid()
