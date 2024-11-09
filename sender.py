from socket import *
from util import *


class Sender:
    ack_num = 0  # setting to 0
    seq_num = 0  # setting to 0
    packet_number = 1  # setting to 1
    status = 1  # can have 3 status, 1 = original message, 2 = retranmission, 3 = socket timed out
    receiver_ip = '127.0.0.1'
    receiver_port = 10440  # as calculated from formula

    def __init__(self):
        """
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()

        Please check the main.py for a reference of how your function will be called.
        """

    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
          app_msg_str: the message string (to be put in the data field of the packet)
          This method will keep transmiting the current message until it acknowledged by the server

        """
        ackreceived = False  # sets it to false
        while ackreceived == False:  # while loop for receiving ack
            ackreceived = self.sendmessage(app_msg_str)  # calls sendmessage method
            self.packet_number += 1  # increasing packet number
            print("\n\n")
        self.seq_num = 1 if self.seq_num == 0 else 0  # if seqnum is 0 then it sets to 1 or otherwise

    def sendmessage(self, app_msg_str):
        sendersocket = self.socket()  # establish connection
        self.printmessage(app_msg_str)  # printing msg based on current state
        packet_send = make_packet(app_msg_str, self.ack_num, self.seq_num)  # creating packet
        print("packet created: {0}".format(packet_send))  # print packet created

        ackreceived = False
        # tryexcept block
        try:
            sendersocket.send(packet_send)  # sending packet
            print("packet num.{0} is successfully sent to the receiver".format(self.packet_number))

            receivedpacket = sendersocket.recv(1024)  # receives response for receiver
            receivedseq = extract_seq_num(receivedpacket)  # extracting seqnum

            ackreceived = receivedseq == self.seq_num  # if equals
            if ackreceived:
                print("packet is received correctly: seq. num = {0} ACK num {1}. all done!".format(self.seq_num,
                                                                                                   self.seq_num))
                self.status = 1  # sets status to 1
            else:
                print("receiver acked the previous pkt, resend!")
                self.status = 2  # sets status to 2

        except Exception as e:
            print("socket timeout! Resend!")
            self.status = 3  # sets status to 3

        sendersocket.close()  # closing socket here
        return ackreceived

    def printmessage(self, app_msg_str):

        if self.status == 1:  # Prints the message based on the status of the cuurent packet
            print("original message string: {0}".format(app_msg_str))
        elif self.status == 2:  ##Prints the message based on the status of the cuurent packet
            print("[ACK-Previous retransmission]: {0}".format(app_msg_str))
        else:
            print("[timeout retransmission]: {0}".format(
                app_msg_str))  # Prints the message based on the status of the cuurent packet

    def socket(self):
        sendersocket = socket(AF_INET, SOCK_STREAM)
        sendersocket.connect((self.receiver_ip, self.receiver_port))  # establishes the connection to the receiver
        sendersocket.settimeout(5)  # setting timeout of 5sec to trigger timeout
        return sendersocket

    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT Change the function name.                    #######
    ####### You can have other functions as needed.                             #######
