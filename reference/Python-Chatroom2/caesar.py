# This file contains two functions for encrypting and decrypting a message (string) using a Caesar shift.
# A user must specify a string and shift size.

'''

Example:
Original Message: Hello! How are you?
Encrypt with shift 6: Nkrru'&Nu}&gxk& u{E
Decrypt with shift -6: Hello! How are you?

'''


# Shifts ASCII values between 32-126 (inclusive).
def caesar_encode(msg, shift):
    encoded = "" # string to store encoded message
    for char in msg: # for each character in the original message
        asciiChar = ord(char) # convert to ascii decimal value
        shiftedChar = asciiChar + shift # add the shift

        if shiftedChar > 126: # if the shift exceeded the ascii range, we need to do math to wrap back around to the beginning
            shiftedChar = ((shiftedChar - 31) % 32) + 32
        
        encoded += chr(shiftedChar) # convert the ascii back to a char and add it to our encoded message
    
    # print("Encoded:", encoded) # return the encoded message
    return encoded



def caesar_decode(msg, shift):
    decoded = "" # string to store encoded message
    for char in msg: 
        asciiChar = ord(char)
        shiftedChar = asciiChar + shift # subtract the shift to decode

        if shiftedChar < 32: # if the shift is lower than the ascii range, we need to do math to wrap back around to the end
            shiftedChar = ((shiftedChar - 31) % 32) + 94

        decoded += chr(shiftedChar) # convert the ascii back to a char and add it to our encoded message
    
    # print("Decoded:", decoded) # return the encoded message
    return decoded



if __name__ == "__main__":
    # Simple test
    msg = "testing! Abcd"
    print(msg)
    enc = caesar_encode(msg, 61)
    caesar_decode(enc, -61)

    # Problem: fails when shift >= 62

