import json
from pathlib import Path


class Database:
    def __init__(
        self,
        filename: str,
        default_data: dict,
        data_folder=None
    ) -> None:

        if data_folder is None:
            project_folder = Path(__file__).resolve().parents[2]
            data_folder = project_folder / "data"

        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(parents=True, exist_ok=True)

        self.file_path = self.data_folder / filename

        if not self.file_path.exists():
            self.save_data(default_data)

        elif self.file_path.stat().st_size == 0:
            self.save_data(default_data)

    def load_data(self) -> dict:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Database content must be a JSON object.")

        return data

    def save_data(self, data: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
