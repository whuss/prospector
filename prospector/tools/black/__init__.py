import subprocess

from prospector.message import make_tool_error_message
from prospector.tools.base import ToolBase

__all__ = ("BlackTool",)


class BlackTool(ToolBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, found_files):
        messages = []

        files = [code_file for code_file in found_files.iter_module_paths()]

        black_return = subprocess.run(["black", "--check", *files], capture_output=True)
        black_errors = black_return.stderr.decode().split("\n")

        for line in black_errors:
            if not line.startswith("would reformat"):
                continue
            code_file = line.split(" ")[2]

            messages.append(
                make_tool_error_message(
                    code_file,
                    "black",
                    "FORMAT",
                    line=1,
                    character=None,
                    message="would reformat",
                )
            )

        return messages
