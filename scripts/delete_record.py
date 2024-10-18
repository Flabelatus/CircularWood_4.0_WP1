"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Callable, List
from __init__ import Scripts
from settings import logger
from workflow.api_client import modify_record

current_module = sys.modules[__name__]


class DeleteDataRow(Scripts):
    def __init__(self, module):
        super().__init__(module=module)
        self.modifiers = {name: modifier for name, modifier in modify_record.get_modifiers_mapping().items()}
        self.menu = self.get_menu()

    def _print_menu(self):
        """Print the available menu options."""
        print("Available Options:")
        for number, option in self.menu.items():
            print(f"{number}: {option[0]}")

    def get_menu(self):
        """Generate and return a menu dictionary of option names."""
        menu = {}
        option_names = []
        for key, option in self.modifiers.items():
            option_name = option().model
            if option_name == "requirements":
                option_name = "design_metadata"
            option_names.append(option_name)
        
        for i in range(len(option_names)):
            replaced_name = option_names[i]
            key = list(self.modifiers.keys())[i]
            option = list(self.modifiers.values())[i]
            menu[i + 1] = replaced_name, key, option
        
        return menu

    def select_option(self, choice: int):
        """Select and return the appropriate modifier based on the user's choice."""
        if choice not in self.menu:
            logger.error("Invalid choice, please select a valid option.")
            return None

        selected_option = self.menu[choice]
        selected_modifier = self.modifiers[selected_option[1]]
        return selected_modifier

    def delete_row(self, row_id_list: List[int], modifier: Callable):
        """Delete a row using the selected modifier."""
        custom_modifier = modifier()

        try:
            custom_modifier.delete(row_id_list)
        except NotImplementedError:
            logger.error("Method not implemented.")
        except Exception as e:
            logger.error(f"An error occurred while deleting row: {str(e)}")

        
def main():

    row_id_list = []

    # Create an instance of DeleteDataRow
    delete_data_row = DeleteDataRow(module=__name__)

    # Print the menu of options
    delete_data_row._print_menu()

    # Get the user's choice
    try:
        choice = int(input("Select a script by number: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Select the appropriate modifier based on choice
    selected_modifier = delete_data_row.select_option(choice)
    if selected_modifier:
        try:
            row_id = int(input("Enter the row ID to delete: "))
            row_id_list.append(row_id)
        except ValueError:
            print("Invalid input. Please enter a valid row ID.")
            return
        
        # Delete the selected row using the modifier
        delete_data_row.delete_row(row_id_list, selected_modifier)


if __name__ == "__main__":
    main()
