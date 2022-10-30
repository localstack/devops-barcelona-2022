lambda: demo-lambda.zip

build: requirements.txt
	mkdir -p build;
	pip install -r requirements.txt -t build/;

demo-lambda.zip: build handler.py cert_template.pdf
	rm -f demo-lambda.zip
	cp handler.py cert_template.pdf build/
	(cd build; zip ../demo-lambda.zip -r .)

clean:
	rm -rf build/ demo-lambda.zip
