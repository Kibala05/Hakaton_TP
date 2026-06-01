class Email:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = filepath.split("/")[-1]
        self.subject = ""
        self.sender = ""
        self.body = ""
        self.category = "unknown"
        self.error = None

    def read(self):
        try:
            with open(self.filepath, encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                self.error = "empty_file"
                return False
            self._parse(content)
            return True
        except UnicodeDecodeError:
            self.error = "binary_file"
            return False    
        except Exception as e:
            self.error = str(e)
            return False

    def _parse(self, content):
        lines = content.split("\n")
        body_started = False
        body_parts = []

        for line in lines:
            if body_started:
                body_parts.append(line)
            elif line.lower().startswith(("subject:", "тема:")):
                self.subject = line.split(":", 1)[1].strip()
            elif line.lower().startswith(("from:", "от кого:")):
                self.sender = line.split(":", 1)[1].strip()
            elif line.strip() == "":
                body_started = True

        self.body = "\n".join(body_parts)

    def get_search_text(self):
        return (self.subject + " " + self.body).lower()
