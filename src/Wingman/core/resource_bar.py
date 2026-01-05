class ResourceBar:
    def __init__(self, current: int, maximum: int):
        self.Current = current
        self.Maximum = maximum

    @staticmethod
    def FromString(value: str) -> 'ResourceBar':
        parts = value.strip().split('/')
        current = int(parts[0].strip())
        maximum = int(parts[1].strip())
        return ResourceBar(current, maximum)

    def __str__(self):
        return f"{self.Current}/{self.Maximum}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ResourceBar):
            return self.Current == other.Current and self.Maximum == other.Maximum

        if isinstance(other, str):
            return self.__str__() == other.replace("/ ", "/")

        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.Current}/{self.Maximum}"
