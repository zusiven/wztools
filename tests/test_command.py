import logging

from wztools.utils.command import run_cmd


class TestRunCmd:
    def test_stdout_stderr_logged_as_warning(self, caplog):
        caplog.set_level(logging.WARNING)
        returncode, stdout, stderr = run_cmd(
            "echo hello && echo world >&2"
        )

        assert returncode == 0
        assert "hello" in stdout
        assert "world" in stderr

        # stdout 和 stderr 的输出都应为 WARNING 级别
        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        warning_messages = [r.message for r in warning_records]
        assert any("hello" in m for m in warning_messages)
        assert any("world" in m for m in warning_messages)

    def test_info_messages_logged_as_info(self, caplog):
        caplog.set_level(logging.INFO)
        run_cmd("echo hi")

        info_messages = [r.message for r in caplog.records if r.levelno == logging.INFO]
        assert any("开始执行命令" in m for m in info_messages)
        assert any("命令执行完成" in m for m in info_messages)

    def test_info_messages_not_warning(self, caplog):
        caplog.set_level(logging.INFO)
        run_cmd("echo hi")

        warning_messages = [r.message for r in caplog.records if r.levelno == logging.WARNING]
        assert not any("开始执行命令" in m for m in warning_messages)
        assert not any("命令执行完成" in m for m in warning_messages)

    def test_return_values(self):
        returncode, stdout, stderr = run_cmd("echo test_output")
        assert returncode == 0
        assert "test_output" in stdout

    def test_timeout(self, caplog):
        caplog.set_level(logging.ERROR)
        returncode, _, _ = run_cmd("sleep 10", timeout=1)
        assert returncode == -1
        error_messages = [r.message for r in caplog.records if r.levelno == logging.ERROR]
        assert any("超时" in m for m in error_messages)
