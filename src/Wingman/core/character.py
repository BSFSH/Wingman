from Wingman.core.status_indicator import StatusIndicator
from Wingman.core.resource_bar import ResourceBar

class Character:
    def __init__(self, name: str,
                        classProfession: str = "",
                        level: int = -1,
                        status: StatusIndicator = StatusIndicator(0),
                        hp: ResourceBar = ResourceBar(-1,-1),
                        fat: ResourceBar = ResourceBar(-1,-1),
                        pow: ResourceBar = ResourceBar(-1,-1),
                        isNewFollower: bool = False):
        self.Name = name.strip()

        self.ClassProfession = classProfession.strip(); 
        self.Level = level
        self.Status = status
        self.Hp = hp
        self.Fat = fat
        self.Pow = pow
        self.IsNewGroupFollower = isNewFollower

    def __repr__(self):
        return f"{self.Name}"
