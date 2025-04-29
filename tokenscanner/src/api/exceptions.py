class TokenNotFoundError(Exception):
    pass


class DEXScreenerAPIException(Exception):
    """Invoked when the DEXScreener API returns an error."""

    pass


class InvalidSolanaAddressError(Exception):
    """Invoked when the Solana address is invalid."""

    pass


def is_valid_solana_address(address: str) -> bool:
    """Check if the given address is a valid Solana address."""

    if address.startswith("0x"):
        # Solana addresses should not start with "0x"
        raise InvalidSolanaAddressError("Solana addresses cannot start with '0x'")

    # A simple check for the length of the address
    # Solana addresses are typically 44 characters long
    return len(address) == 44 and all(
        c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        for c in address
    )
