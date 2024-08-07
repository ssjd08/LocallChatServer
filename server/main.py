from chatserver import ChatServer


if __name__ == "__main__":
    print("in server!")
    chat_server = ChatServer()
    chat_server.listen()
    chat_server.accept()
    chat_server.close()