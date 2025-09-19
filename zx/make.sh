rm -f *.lst *.tap

make() {
    if test -f $1.bas; then
        ~/repos/bas2tap/bas2tap -q -s$1 $1.bas $1.bas.tap
    fi
    if test -f $1.asm; then
        sjasmplus --lst=$1.asm.lst $1.asm
    fi
}

#make proba
#make life
make flife

