
download:
	gmvn jars download --group dev.zio --artifact zio-test_2.13 --version 1.0.15 --outdir lib --verbose

compile:
	mkdir -p out
	scalac -d out -classpath 'out:lib/*' *.scala

test: compile
	scala -classpath 'out:lib/*' chess.TestChess
