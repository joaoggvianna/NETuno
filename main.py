from core.assistant import Assistant


def main() -> None:
    """Run the Jarvis command-line interface."""
    assistant = Assistant()

    while True:
        try:
            user_input = input("JARVIS > ")
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais.")
            break

        result = assistant.process_command(user_input)
        print(result.message)

        if result.should_exit:
            break


if __name__ == "__main__":
    main()
