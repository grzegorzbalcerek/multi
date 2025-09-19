readme:
	cat README.md

clean:
	rm *.js

cleanall: clean
	rm -rf node_modules

etest: ecompile
	node_modules/.bin/jest *.test.js --color=false

ecompile:
	tsc *.ts -t ES2020 --pretty false -m commonjs

compile:
	tsc *.ts -t ES2020 -m commonjs

init:
	npm install --save-dev ts-jest
	npm install --save-dev @jest/globals

test: compile
	node_modules/.bin/jest *.test.js
