import os
from typer.testing import CliRunner
from expense_tracker.cli import app
from expense_tracker.config import Config
from expense_tracker.db.db_client import DBClient


class TestCli:
    def setup_method(self):
        self.runner = CliRunner()
        os.environ[Config.ENV_DB_NAME] = "test_expenses.db"

    def teardown_method(self):
        # the tuple returned by PRAGMA database_list has the format (seq, name, file)
        db_path = DBClient.get_connection().execute(
            "PRAGMA database_list;").fetchone()[2]
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_init_should_initialize_db(self):
        del os.environ[Config.ENV_DB_NAME]
        result = self.runner.invoke(app, ["init", "--name", "test_user"])
        assert result.exit_code == 0
        assert "Expense tracker initialized for" in result.output
        os.environ[Config.ENV_DB_NAME] = "test_expenses.db"

    def test_init_should_initialize_db_with_env_variable(self):
        result = self.runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Expense tracker initialized for" in result.output

    def test_init_should_handle_db_initialization_error(self):
        del os.environ[Config.ENV_DB_NAME]
        result = self.runner.invoke(app, ["init"])
        assert result.exit_code == 1
        assert "Error:" in result.output
        os.environ[Config.ENV_DB_NAME] = "test_expenses.db"
