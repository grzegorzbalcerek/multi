
clean:
	rm -rf __pycache__

black:
	black *.py

isort:
	isort *.py

format: black isort

SOURCES=color.py field.py figure.py figure_move.py move.py board.py game.py
UNITTESTS=color_test.py field_test.py figure_test.py figure_move_test.py board_test.py game_test.py

test: doctest unittest

doctest: $(SOURCES)
	python3 -m doctest $^

unittest: $(SOURCES) $(UNITTESTS)
	python3 -m unittest $^

