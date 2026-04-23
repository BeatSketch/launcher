import platform
import os
import subprocess as sp


class BeatSketchInstance:
    """Launch a BeatSketch VR instance with the current settings"""

    def __init__(self) -> None:
        self._process = sp.Popen(
            self._command(["test.lua", "TEST"]),
            text=True,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            stdin=sp.PIPE,
        )

    def __del__(self) -> None:
        self.await_close()

    def _command(self, args: list[str]) -> list[str]:
        if platform.system() == "Linux":
            # Detect Wayland
            if (
                os.getenv("XDG_BACKEND") == "wayland"
                or os.getenv("XDG_SESSION_TYPE") == "wayland"
            ):
                return ["gamescope", "lua"] + args
            return ["lua"] + args
        elif platform.system() == "Mac":
            return ["lua"] + args
        else:
            # FIXME: Handle for Windows (and Mac if we support that)
            # TODO: This is currently set to lanch a non-existent executable
            return ["start BeatSketch.exe"] + args

    def read(self) -> str:
        """Read a line from stdout from the BeatSketch process.
        Will hang until new line becomes available

        Returns:
            The line that was read
        """
        if self._process.stdout:
            return self._process.stdout.readline()
        return ""

    def read_stderr(self) -> str:
        """Read from the stderr from the BeatSketch process.
        Will hang until new line becomes available

        Returns:
            The line that was read
        """
        if self._process.stderr:
            return self._process.stderr.readline()
        return ""

    def write(self, msg: str) -> None:
        """Write to the stdin of the BeatSketch process

        Args:
            msg: The message to send
        """
        if self._process.stdin:
            self._process.stdin.write(msg + "\n")
            self._process.stdin.flush()

    def await_launch(self) -> None:
        """Wait for the VR application to finish initialization"""
        while self.read() != "TEST\n":
            pass

    def await_close(self) -> int:
        """Wait for the VR application to exit

        Returns:
            The exit code of the application
        """
        self._process.communicate()
        return self._process.wait()
