
F=Hello.class

all: $(F) inspect

%.class: %.java
	javac $<

clean:
	rm -f *.class *.dump *.beam

inspect.beam: inspect.erl
	erlc $<

inspect: inspect.beam
	erl -noshell -s inspect main $(F) -s init stop
