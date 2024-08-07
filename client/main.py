import socket 
from queue import Queue
from threading import Thread

server_ip = "127.0.0.1"
server_host = 9090

def get_input_from_user(queue:Queue)->None:
    print("ready to send data to server!")
    while True:
        data = input()
        queue.put(data)


def get_data_from_server(socket)->None:
    while True:
        server_data = socket.recv(2048)
        print(server_data.decode())
    
if __name__ == "__main__":
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_host))
    
    queue = Queue()
    
    massage_queue_thread = Thread(target=get_input_from_user, args=(queue,))
    massage_queue_thread.start()
    
    get_data_thread = Thread(target=get_data_from_server, args=(s,))
    get_data_thread.start()
    
    # send_data_thread = Thread(target=send_data_to_server, args=(queue, socket, massage_queue_thread, get_data_thread))
    # send_data_thread.start()
    # send_data_thread.join()
    
    #send data thread:
    while True:
        try:
            data = queue.get(timeout=5)
            s.send(data.encode())
            if data == "q" or data == "quit":
                print("closing connection!")
                break
            
        except : 
            continue
        
    massage_queue_thread.join()
    get_data_thread.join() 
    s.close()