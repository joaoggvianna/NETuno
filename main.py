from core.assistant import Assistant
from database.database import initialize_database


def main() -> None:
    """Run the Jarvis command-line interface."""
    initialize_database()
    assistant = Assistant()

    while True:
        try:
            user_input = input("NETUNO > ")
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais.")
            break

        result = assistant.process_command(user_input)
        print(result.message)

        if result.should_exit:
            break


if __name__ == "__main__":
    main()
