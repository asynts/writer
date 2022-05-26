class Node:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def append_child(self, child: "Node"):
        self.children.append(child)
        return child
    
    def to_string_header(self):
        return f"{self.name}()"

    def to_string(self, *, indent=0, prefix=""):
        result = ""

        result += " " * indent
        result += prefix + self.to_string_header() + "\n"

        for child in self.children:
            result += child.to_string(indent=indent + 1, prefix="<child> ")
        
        return result

    def __str__(self):
        return self.to_string()
