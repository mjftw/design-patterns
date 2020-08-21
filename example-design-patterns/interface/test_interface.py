from .interface import Dog, Duck, IAnimal, IMovable, ISoundable


def test_IAnimal_should_implement_IMovable():
    assert issubclass(IAnimal, IMovable)


def test_IAnimal_should_implement_ISoundable():
    assert issubclass(IAnimal, ISoundable)


def test_Dog_should_implement_IAnimal():
    assert issubclass(Dog, IAnimal)


def test_Duck_should_implement_IAnimal():
    assert issubclass(Duck, IAnimal)


def test_Dog_should_make_bark_sound(dog, capsys):
    dog.make_sound()
    captured = capsys.readouterr()
    assert 'Bark!' in captured.out


def test_Dog_should_do_move_walk(dog, capsys):
    dog.move()
    captured = capsys.readouterr()
    assert 'Walk' in captured.out


def test_Duck_should_make_bark_sound(duck, capsys):
    duck.make_sound()
    captured = capsys.readouterr()
    assert 'Quack!' in captured.out


def test_Duck_should_do_move_walk(duck, capsys):
    duck.move()
    captured = capsys.readouterr()
    assert 'Waddle' in captured.out


