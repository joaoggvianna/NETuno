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


if __name__ == "__main__":
    unittest.main()
