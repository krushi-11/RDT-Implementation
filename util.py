def create_checksum(packetchecksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    k = 16 #setting the length of Checksum
    sum = sum_of_words(packetchecksum) #this calculates the words in packetchecksum

    if (len(sum) > k): #checking if sum is greater than k
        x = len(sum) - k #if sum is greater than 16 it calculates the excess bits and storing it in x
        sum = bin(int(sum[0:x], 2) + int(sum[x:], 2))[2:] #it is spliting the string into two parts and converting them into int and adding them and again converting it into binary

    if (len(sum) < k): #checking if sum is less than k
        sum = '0' * (k - len(sum)) + sum #if sum is less then it is adding zeroes in front

    Checksum = '' #empty string using for inverted checksum
    for i in sum: #this starts loop for scanning each character in sum
        if (i == '1'): #checks if i=1
            Checksum += '0' #if 1 then setting it to 0
        else:
            Checksum += '1' #if not 1 means it is 0 then setting it to 1

    return int(Checksum, 2).to_bytes(2, 'big') #converting binary to int and then converts it into 2byte big-endian


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    sum = create_checksum(packet) #calculating checksum for packet and assigning to the sum variable
    return 0 == int.from_bytes(sum, "big") #checking if checksum is 0 then it will be true


def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    initial_checksum = 0 #getting checksum in this variable and initialize it to 0
    packet = list() #creating empty list
    packet.append(b'COMP') #appending the byte to the list
    packet.append(b'NETW') #appending the byte to the list
    packet.append(initial_checksum.to_bytes(2, 'big'))  # appending the checksum which is 0 and converted it to 2byte big-endian
    length = 12 + len(data_str) #calculates total length of packet
    packet.append(length(length, ack_num, seq_num)) #appending the 3 info to list
    packet.append(data_str.encode()) #encoding the msg and appending it to list
    packetchecksum = b''.join(packet) #joining packet into single bytes object excluding checksum
    checksum = create_checksum(packetchecksum) #calculates checksum for packet
    packet[2] = checksum #this changes the third element with actual checksum
    packet_with_checksum = b''.join(packet) # again joining all components to list
    return packet_with_checksum #returns full packet


def length(length, ack_num, seq_num):
    #this represents 2bytes
    length = length << 1 #shifting the bits to left by one
    length = length | ack_num #this combines ack_num with packetlength
    length = length << 1 #again left shift by one
    length = length | seq_num #this combines seq_num with packetlength
    return length.to_bytes(2, 'big') #converts 16 bit packet to 2byte big-endian


def sum_of_words(packet):
    #grouping the packet into 16bits
    packet_array = list(packet) #converts packet into list
    sum = 0 # setting value to 0
    for i in range(0, len(packet_array), 2): #loop for packet array with spacing of 2, to group the bytes into 16bit words
        w1 = packet_array[i] & 0xFF # storing the first 8 bits
        w1 = w1 << 8 #this shifts 8 bits of w1
        w2 = 0 #initialize to 0
        if i + 1 < len(packet_array): #checks if there is another byte available for second byte
            w2 = packet_array[i + 1] & 0xFF #if available it stores it in w2
            sum += w1 + w2 #total

    ## substringing because bin() returns string with 0b prefixed
    sum = bin(sum)[2:] #converts decimal sum to binary string and [2:] is used to remove 0b
    return sum


def extract_message(packet):
    #This method assumes the first 12 bytes are header + checksum and the message part starts only from the 13th byte
    packet_array = list(packet) #converts packet into list and separates each byte
    return "".join(map(chr, packet_array[12:])) #process the elements from 13 and map function is used to apply chr to each byte and then join used to concatenate into single string


def extract_seq_num(packet):
    #returns the single bit for seqnum
    packet_array = list(packet) #converts packet into list and separates each byte
    byte_with_sequence = packet_array[11] #extract byte at 11 and stores it
    return byte_with_sequence & 0x01 #adding bitmask to isolate





###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should not make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######
