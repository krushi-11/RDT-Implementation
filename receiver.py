from socket import *
from time import sleep
from util import *
#No other imports allowed

receiver_port = 10100+(4196840)%500
receiver_socket = socket(AF_INET, SOCK_STREAM)


receiver_socket.bind(('', receiver_port)) # Binding server socket
receiver_socket.listen(15) #listening for 15sec
packet_number = 1 #setting packet number to 1
ack_num = 1 #setting acknum to 1

def rdt_receive(packet_number, seqreceived, msg):
    if packet_number % 6 == 0: #checks the packet number if the packet is 6 then it prints packet loss and sender have to retransmit the packet
        print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
        sleep(5) #setting the receiver to sleep to trigger timeout
        return None
    elif packet_number % 3 == 0: #checks the packet number if the packet is 3 then it prints corrupted packet and sender has to retransmit the same packet created
        print("simulating packet bit errors/corrupted: ACK the previous packet")
        return 1 if seqreceived == 0 else 0 #after retransmitting ,the seqnum have to be changed
    else: #if not 6 neither 3 received then this statement will run
        print("packet is expected, message string delivered: {0}".format(msg))
        print("packet is delivered, now creating and sending the ACK packet...")
        return seqreceived

while True:
    sendersocket, sender_addr = receiver_socket.accept() #accepting the data from sender
    packet = sendersocket.recv(1024) #stores it in packet
    print("packet num.{0} received: {1}".format(packet_number, packet)) #printing the received data
    verifychecksum = verify_checksum(packet) #verifying checksum from the received packet
    msg = extract_message(packet) #extracting message and storing it in msg
    seqreceived = extract_seq_num(packet) #extracting seqnum and storing it to seqreceived
    seq_send = rdt_receive(packet_number, seqreceived, msg) #storing the result of rdt_receive in seq_send variable
    if seq_send != None: #if seq_send is none
        packetsend = make_packet(msg, ack_num, seq_send) #if its none then create packet with msg,acknum,seqsend
        sendersocket.send(packetsend) #and then sending that packet to sender
    print("all done for this packet!\n\n")
    packet_number += 1 #increasing the packet number by 1
    with open("received_pkt.txt","a") as file : #opening the text file with named received_pkt.txt
            file.write(f"{packet}\n") #this writes the packet received from sender and storing it to text file