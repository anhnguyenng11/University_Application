import json
from pathlib import Path

class Database:
    """
    A class to handle reading and writing data to a JSON file, simulating a simple database.
    Methods:
    - __init__: Initializes the Database with a filename, default data, and an optional data folder.
    - load_data: Loads the data from the database file into a dictionary.
    - save_data: Saves the data to the database file.
    """
    def __init__(
        self,
        filename: str,
        default_data: dict,
        data_folder=None
    ) -> None:

        if data_folder is None:
            project_folder = Path(__file__).resolve().parents[2]
            data_folder = project_folder / "data"

        self._data_folder = Path(data_folder)
        self._data_folder.mkdir(parents=True, exist_ok=True)

        self._file_path = self._data_folder / filename

        if not self._file_path.exists():
            self.save_data(default_data)

        elif self._file_path.stat().st_size == 0:
            self.save_data(default_data)

    def load_data(self) -> dict:
        """
        Loads the data from the database file into a dictionary.
        Returns: A dictionary containing the data.
        """
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Database content must be a JSON object.")

        return data

    def save_data(self, data: dict) -> None:
        """
        Saves the data to the database file.
        Args:
            data (dict): The data to be saved.
        """
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
