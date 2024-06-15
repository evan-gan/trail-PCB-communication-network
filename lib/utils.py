import urandom


def random_string(length):
    # Define the characters to choose from
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    # Create a random string of the specified length
    result = ''.join(characters[urandom.getrandbits(
        6) % len(characters)] for _ in range(length))

    return result
