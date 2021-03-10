from .server import GreetingsGenerator


def test_greetings_with_name():
    values = {'age': ['12'], 'name': ['Jan']}
    generator = GreetingsGenerator(values)
    assert generator.generate() == "hello Jan"


def test_greetings_without():
    values = {'age': ['12']}
    generator = GreetingsGenerator(values)
    assert generator.generate() == "hello world"
