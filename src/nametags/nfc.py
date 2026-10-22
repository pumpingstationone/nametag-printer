"""Read the UID of an NFC tag from a connected USB reader."""

from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import (
    CardConnectionException,
    CardRequestTimeoutException,
    SmartcardException,
)
from smartcard.System import readers
from smartcard.util import toHexString

# Get UID (per PC/SC WG Part 3)
GET_UID_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]

# Success code (per ISO 7816-4)
GET_UID_APDU_OK = (0x90, 0x00)


def get_uid_from_connection(connection) -> str | None:
    """Transmit the GET UID APDU over an existing card connection.

    Returns the UID as a hex string, or None if the card/reader
    doesn't support the command.
    """
    try:
        response, sw1, sw2 = connection.transmit(GET_UID_APDU)
    except CardConnectionException as e:
        raise RuntimeError(f"Failed to communicate with card: {e}") from e

    if (sw1, sw2) == GET_UID_APDU_OK and response:
        return toHexString(response).replace(" ", "").upper()
    return None


def read_uid(newcardonly: bool = False, timeout: float | None = None) -> str:
    """
    Wait for a card and return its UID.

    Use timeout to limit the total wait in seconds, or None to wait indefinitely.

    Returns the UID as an uppercase hex string.

    Raises RuntimeError if no reader is found or the wait times out.
    """
    try:
        if not readers():
            raise RuntimeError("No PC/SC readers found.")
    except Exception as e:
        raise RuntimeError(f"Could not access PC/SC service: {e}") from e

    request = CardRequest(newcardonly=newcardonly, timeout=timeout)
    try:
        service = request.waitforcard()
    except CardRequestTimeoutException:
        raise RuntimeError(f"Timed out after {timeout}s waiting for a card.")

    connection = service.connection
    try:
        connection.connect()
    except SmartcardException as e:
        raise RuntimeError(f"Card vanished before connect: {e}") from e

    try:
        uid = get_uid_from_connection(connection)
    finally:
        try:
            connection.disconnect()
        except CardConnectionException:
            pass

    if uid is None:
        raise RuntimeError("Card does not support reading its UID.")

    return uid
