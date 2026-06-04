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
        print(
            f"\n>>> Welcome! {user.name} has joined the {self.room_name}. <<<")

    def leave(self, user):
        self.users.remove(user)
        print(f"\n>>> {user.name} left the {self.room_name} <<<")

    def add_message(self, message):
        self.history.append(message)

    def show_history(self):
        print(f"\n=== Chat History for {self.room_name} ===")
        if not self.history:
            print("No messages yet.")
        for msg in self.history:
            print(f"{msg.sender_name}: {msg.content}")
        print("================\n")

# The main function initializes the chat room and allows the user to
# interact with it through a simple command-line interface.


def main():
    # Initialize the chat room and a dictionary to keep track of active users.
    my_chatroom = ChatRoom("Study Group")
    active_users = {}

    print("--- Welcome to the Study Group Chat ---")

    while True:
        # Display the menu options for the user to interact with the chat system.
        print("\n[1] Join [2] Chat [3] History [4] Leave [5] Exit")

        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter your name: ")
            if name not in active_users:
                new_user = User(name)
                active_users[name] = new_user
                my_chatroom.join(new_user)
                print(
                    f"Current users in the chat: {[user.name for user in my_chatroom.users]}")
            else:
                print("User already in room.")

        elif choice == '2':
            my_message = input("Type 'Name: Message' -> ")
            if ":" in my_message:
                name_part, text_part = my_message.split(":", 1)  # Parse once
                # strip() removes accidental spaces
                name_part = name_part.strip()

                if name_part in active_users:
                    # We still use the Object to send it!
                    active_users[name_part].send_text(
                        text_part.strip(), my_chatroom)
                else:
                    print("User not found.")

        elif choice == '3':
            my_chatroom.show_history()

        elif choice == '4':
            leaver_name = input("Who is leaving? ").strip()

            # Check if the user exists in our local dictionary
            if leaver_name in active_users:
                user_to_remove = active_users[leaver_name]

                # chatroom.leave() will remove the user from the chatroom's list of users and print a message
                my_chatroom.leave(user_to_remove)

                # After leaving the chatroom, we also remove the user from our local dictionary of active users
                del active_users[leaver_name]
                print(f"Success: {leaver_name} has been disconnected.")

            else:
                print(
                    f"Error: '{leaver_name}' is not currently in the session.")

        elif choice == '5':
            print("Closing chatroom...")
            break


# Main entry point of the program, calling the main function to start the chat system.
if __name__ == "__main__":
    main()
