# Create a Chat System using Object-Oriented Programming (OOP) concepts.
# You need to create the following classes: User, Message, ChatRoom
# The system should implement the following functionalities:
# Sending messages, Viewing chat history, User joining and leaving the chat room
# The system allows users to send messages, view the chat history, and manage user participation in the chat room.

# The Message class represents a message sent by a user, containing the sender's name and the
# content of the message.
class Message:
    def __init__(self, sender_name, content):
        self.sender_name = sender_name
        self.content = content

# The User class represents a user in the chat system, allowing them to send messages to a chat room.


class User:
    def __init__(self, name):
        self.name = name

    def send_text(self, text, chat_room):
        # The user creates a Message and gives it to the ChatRoom
        new_msg = Message(self.name, text)
        chat_room.add_message(new_msg)

# The ChatRoom class manages the chat room, allowing users to join and leave, and keeps a history of messages sent in the room.


class ChatRoom:
    def __init__(self, room_name):
        self.room_name = room_name
        self.users = []
        self.history = []

    def join(self, user):
        self.users.append(user)
        print(f"\n--- {user.name} joined the {self.room_name} ---")

    def leave(self, user):
        self.users.remove(user)
        print(f"\n--- {user.name} left the {self.room_name} ---")

    def add_message(self, message):
        self.history.append(message)

    def show_history(self):
        print(f"\n=== Chat History for {self.room_name} ===")
        if not self.history:
            print("No messages yet.")
        for msg in self.history:
            print(f"{msg.sender_name}: {msg.content}")
        print("================\n")


# The main function initializes the chat room and allows the user to interact with it through a simple command-line interface.
if __name__ == "__main__":
    # Create the room object once
    my_chatroom = ChatRoom("Study Group")

    # Get the user's name from the keyboard
    visitor_name = input("Enter your username: ")
    active_user = User(visitor_name)
    my_chatroom.join(active_user)

    while True:
        print("\nMain Menu: [1] Chat [2] History [3] Exit")
        choice = input("Select an option: ")

        if choice == '1':
            text = input("Type your message: ")
            active_user.send_text(text, my_chatroom)
        elif choice == '2':
            my_chatroom.show_history()
        elif choice == '3':
            my_chatroom.leave(active_user)
            print("Program terminated.")
            break
        else:
            print("Invalid input, try again.")
