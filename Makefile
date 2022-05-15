build:
	python3 resolution.py
	./make_png.sh
	python3 make_gif.py

clean:
	rm dot/* png/*