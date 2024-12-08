import re

from workflow.production_run import logger


class RAPIDParser:
    def __init__(self, content: str):
        """
        Initialize the RAPIDParser object with RAPID content.
        """
        self.in_between_marker = '\nINBETWEEN\n'
        self.content = content
        self.lines = content.splitlines()
    
    def _insert_marker_flag(self, line_index: int, marker: str):
        """
        Insert a marker at a specific line index.
        """
        if 0 <= line_index < len(self.lines):
            self.lines[line_index] = marker + self.lines[line_index]
        else:
            raise IndexError("Line index out of range.")

    def _sanity_check(self):
        """
        Perform basic sanity checks to ensure the RAPID content is well-formed.
        """
        if not self.content.strip():
            raise ValueError("RAPID code content is empty.")
        if "PROC main()" not in self.content:
            raise ValueError("Main procedure 'PROC main()' not found.")

    def _parse_rapid(self):
        """
        Parse the RAPID content to extract various components.
        Returns:
            dict: A dictionary containing extracted components.
        """
        self._sanity_check()

        variables = []
        io_declarations = []
        instructions = []
        main_process = []
        line_index_map = {}

        in_main = False
        for idx, line in enumerate(self.lines):
            stripped = line.strip()
            line_index_map[idx] = stripped

            if stripped.startswith("VAR") or stripped.startswith("PERS"):
                variables.append(stripped)
            elif "->" in stripped:  # Example for I/O declarations
                io_declarations.append(stripped)
            elif "PROC main()" in stripped:
                in_main = True
            elif in_main and "ENDPROC" in stripped:
                in_main = False
            elif in_main:
                main_process.append(stripped)
            else:
                instructions.append(stripped)

        return {
            "var": variables,
            "io": io_declarations,
            "instructions": instructions,
            "proc": main_process,
            "line_index_map": line_index_map,
        }

    def update_rapid_variable(self, variable_name: str, new_value: str):
        """
        Update the value of a variable in the RAPID code.
        """
        pattern = re.compile(rf"({variable_name}\s*:=\s*)([^;]+)(;)")
        for idx, line in enumerate(self.lines):
            if _ := pattern.search(line):
                self.lines[idx] = pattern.sub(rf"\1{new_value}\3", line)
                return
        raise ValueError(f"Variable '{variable_name}' not found.")

    def _remove_program_line(self, line_index: int):
        """
        Remove a specific line from the RAPID content.
        """
        if 0 <= line_index < len(self.lines):
            del self.lines[line_index]
        else:
            raise IndexError("Line index out of range.")

    def add_comment(self, comment: str, line_index: int):
        """
        Add a comment at a specific line index.
        """
        if 0 <= line_index < len(self.lines):
            self.lines[line_index] = f"! {comment} {self.lines[line_index]}"
        else:
            raise IndexError("Line index out of range.")

    def remove_comment(self, line_index: int):
        """
        Remove a comment from a specific line.
        """
        if 0 <= line_index < len(self.lines):
            self.lines[line_index] = re.sub(r"^\s*!\s.*", "", self.lines[line_index])
        else:
            raise IndexError("Line index out of range.")

    def remove_home_position(self, marker: str = "home"):
        """
        Remove home position from the RAPID content based on a marker.
        """
        self.lines = [line for line in self.lines if marker.lower() not in line.lower()]

    def split_rapid(self):
        logger.debug('RAPID code splitted into parts')
        return self.content.split(self.in_between_marker)

    def __str__(self):
        """
        Convert the RAPID code object back to a string representation.
        """
        return "\n".join(self.lines)

