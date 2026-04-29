import platform
import os
import subprocess as sp


class NoAliveSubprocessException(Exception):
    pass


class BeatSketchInstance:
    """Launch a BeatSketch VR instance with the current settings"""

    def __init__(self, unix_cmd: list[str], windows_cmd: list[str], app_args: list[str] = []) -> None:
        self._main_name_unix = unix_cmd
        self._main_name_windows = windows_cmd
        self._process = sp.Popen(
            self._command(["TEST"] + app_args),
            text=True,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            stdin=sp.PIPE,
        )
        self._alive = True

    def __del__(self) -> None:
        self.await_close()

    def _command(self, args: list[str]) -> list[str]:
        if platform.system() == "Linux":
            # Detect Wayland
            if (
                os.getenv("XDG_BACKEND") == "wayland"
                or os.getenv("XDG_SESSION_TYPE") == "wayland"
            ):
                return ["gamescope"] + self._main_name_unix + args
            return self._main_name_unix + args
        elif platform.system() == "Mac":
            return self._main_name_unix + args
        else:
            # FIXME: Handle for Windows (and Mac if we support that)
            # TODO: This is currently set to lanch a non-existent executable
            return ["start"] + self._main_name_windows + args

    def check_alive(self) -> bool:
        """Check if the process is still alive

        Returns:
            True if so, False otherwise

        Raises:
            NoAliveSubprocessException: On repeated calls while unalive, raises this exception
        """
        if not self._alive:
            raise NoAliveSubprocessException()

        self._alive = self._process.poll() is None
        return self._alive

    def read(self) -> str:
        """Read a line from stdout from the BeatSketch process.
        Will hang until new line becomes available

        Returns:
            The line that was read or empty string.
            If the process has quit, returns "proc:has-quit"
        """
        if not self.check_alive():
            return "proc:has-quit"
        if self._process.stdout:
            data = self._process.stdout.readline()
            if data == "proc:instr-await\n":
                self.write("proc:last-instr")
                return ""
            return data
        return ""

    def read_stderr(self) -> str:
        """Read from the stderr from the BeatSketch process.
        Will hang until new line becomes available

        Returns:
            The line that was read
            If the process has quit, returns "proc:has-quit"
        """
        if not self.check_alive():
            return "proc:has-quit"
        if self._process.stderr:
            return self._process.stderr.readline()
        return ""

    def write(self, msg: str) -> bool:
        """Write to the stdin of the BeatSketch process
            USE SPARINGLY! (Can cause the child process to hang)

        Args:
            msg: The message to send
        Returns:
            True if successful, False if exited or failed for other reason
        """
        if not self.check_alive():
            return False
        if self._process.stdin:
            self._process.stdin.write(msg + "\n")
            self._process.stdin.flush()
            return True
        return False

    def await_launch(self, msg: str) -> None:
        """Wait for the VR application to finish initialization

        Args:
            msg: The message that is sent on completed initialization
                 NOTE: Linebreak is appended automatically if not present
        """
        if not msg.endswith("\n"):
            msg = msg + "\n"

        while self.read() != msg:
            pass

    def await_close(self) -> int:
        """Wait for the VR application to exit

        Returns:
            The exit code of the application
        """
        self._process.communicate()
        return self._process.wait()
