import re

def remove_prefix(s: str) -> str:
    return re.sub(r"^\d+\.\s*", "", s)

s1 = "1. fo.o"
s2 = "42. b.ar"

print(remove_prefix(s1))  # prints "fo.o"
print(remove_prefix(s2))  # prints "b.ar"