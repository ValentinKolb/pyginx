import jinja2
from dataclasses import dataclass


@dataclass(frozen=True)
class Test:
    text1: str
    text2: str


if __name__ == '__main__':
    test_class = Test("das ist ein test", "Das ist auch ein test")

    template = jinja2.Template("""{{ test.text1 }}
                               
                               {{ test.text2}}""")

    print(template.render(test=test_class))
