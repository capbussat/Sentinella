# settings.py

from pathlib import Path
import yaml

class Settings:
    def __init__(self, filename="settings.yaml"):
        self.filename = Path(filename)
        self.data = self._load()

    def _load(self):
        if not self.filename.exists():
            raise FileNotFoundError(
                f"No s'ha trobat el fitxer de configuració: {self.filename}"
            )

        with open(self.filename, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def settings(self):
        return self.data.get("settings", {})

    @property
    def buttons(self):
        return self.data.get("buttons", [])

    def reload(self):
        """Recarrega la configuració des del fitxer."""
        self.data = self._load()


# Global instance
settings = Settings()
print("Settings loaded")
# Logging
# print(" type:" + settings.settings["type"])
# print(" ssh_ser:" + settings.settings["ssh_user"])
# print(" ssh_timeout:" + str( settings.settings["ssh_timeout"]))
# print(" max_threads:" + str(settings.settings["max_threads"]))
# print(" data: " + settings.settings["directory"]["data"])
# print(" binary: " + settings.settings["directory"]["binary"])
# print(" settings: " + settings.settings["directory"]["settings"])
# for button in settings.buttons:
#     print("title: "  + button["title"])
#     print("command: " + button["command"])
#     print("unique_word: " + button["unique_word"])


