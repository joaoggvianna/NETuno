import unittest

from core.models import CommandResult, Intent, ParsedCommand
from core.router import Router


class RouterTestCase(unittest.TestCase):
    def test_dispatches_command_to_registered_handler(self) -> None:
        expected_result = CommandResult(success=True, message="Handler executado.")

        def handler(command: ParsedCommand) -> CommandResult:
            self.assertEqual(command.intent, Intent.GET_TIME)
            return expected_result

        router = Router(handlers={Intent.GET_TIME: handler})
        command = ParsedCommand(Intent.GET_TIME, "que horas são")

        self.assertEqual(router.dispatch(command), expected_result)

    def test_returns_failure_for_unknown_command(self) -> None:
        router = Router()
        command = ParsedCommand(Intent.UNKNOWN, "faça café")

        result = router.dispatch(command)

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Não reconheci esse comando.")
        self.assertFalse(result.should_exit)

    def test_routes_system_status_intent(self) -> None:
        expected_result = CommandResult(True, "Status tratado.")
        router = Router(
            handlers={Intent.GET_SYSTEM_STATUS: lambda command: expected_result}
        )

        result = router.dispatch(
            ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")
        )

        self.assertEqual(result, expected_result)

    def test_routes_open_app_intent(self) -> None:
        expected_result = CommandResult(True, "Aplicativo tratado.")
        router = Router(handlers={Intent.OPEN_APP: lambda command: expected_result})

        result = router.dispatch(
            ParsedCommand(Intent.OPEN_APP, "abrir vscode", target="vscode")
        )

        self.assertEqual(result, expected_result)

    def test_routes_open_website_intent(self) -> None:
        expected_result = CommandResult(True, "Site tratado.")
        router = Router(
            handlers={Intent.OPEN_WEBSITE: lambda command: expected_result}
        )

        result = router.dispatch(
            ParsedCommand(Intent.OPEN_WEBSITE, "abrir youtube", target="youtube")
        )

        self.assertEqual(result, expected_result)

    def test_routes_note_intents(self) -> None:
        for intent in (
            Intent.CREATE_NOTE,
            Intent.LIST_NOTES,
            Intent.DELETE_NOTE,
        ):
            with self.subTest(intent=intent):
                expected_result = CommandResult(True, "Nota tratada.")
                router = Router(handlers={intent: lambda command: expected_result})

                result = router.dispatch(ParsedCommand(intent, "comando de nota"))

                self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
