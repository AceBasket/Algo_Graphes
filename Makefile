TEXT ?= graphe_intermediaire.txt

build:
	python3 resolution.py $(TEXT)
	./make_png.sh
	python3 make_gif.py

clean:
	rm dot/* png/*