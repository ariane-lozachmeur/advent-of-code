
def run_steps(subject_number, loop_size):
    '''Set the value to itself multiplied by the subject number.
    Set the value to the remainder after dividing the value by 20201227.'''
    value = 1
    for n in range(loop_size):
        value *= subject_number
        divider = 20201227
        value = value % divider
    return value

def find_loop_size(subject_number, final_value):
    current_loop = 0
    value = 1
    divider = 20201227
    while value != final_value:
        value *= subject_number
        value = value % divider
        current_loop += 1

    return current_loop, value

def reverse_engineer_handshake(subject_number, card_public_key, door_public_key):
    card_secret_loop_size, _ = find_loop_size(subject_number, card_public_key)
    door_secret_loop_size, _ = find_loop_size(subject_number, door_public_key)
    print(card_secret_loop_size, door_secret_loop_size)
    encryption_key1 = run_steps(door_public_key, card_secret_loop_size)
    encryption_key2 = run_steps(card_public_key, door_secret_loop_size)
    print(encryption_key1, encryption_key2)

def handshake():
    '''
    1. The card transforms the subject number of 7 according 
    to the card's secret loop size. The result is called the card's public key.
    
    2. The door transforms the subject number of 7 according to the door's secret 
    loop size. The result is called the door's public key.
    
    3. The card and door use the wireless RFID signal to transmit 
    the two public keys (your puzzle input) to the other device. 
    Now, the card has the door's public key, and the door has the 
    card's public key. Because you can eavesdrop on the signal, 
    you have both public keys, but neither device's loop size.
    
    4. The card transforms the subject number of the door's public 
    key according to the card's loop size. The result is the encryption key.
    
    5. The door transforms the subject number of the card's public key according 
    to the door's loop size. The result is the same encryption key as 
    the card calculated.'''

    card_secret_loop_size = 1 # we don't know this
    door_secret_loop_size = 1 # we don't know this
    card_public_key = run_steps(7, card_secret_loop_size) # we know this
    door_public_key = run_steps(7, door_secret_loop_size) # we know this
    encryption_key1 = run_steps(door_public_key, card_secret_loop_size)
    encryption_key2 = run_steps(card_public_key, door_secret_loop_size)


if __name__=="__main__":
    card_public_key = 9717666
    door_public_key = 20089533
    # card_public_key = 5764801
    # door_public_key = 17807724
    reverse_engineer_handshake(7, card_public_key, door_public_key)


