# LocalStack DevOps Barcelona contest

Here's the code of the lambda you'll run to enter the raffle.

## Enter the contest

To run the code, simply download the `demo-lambda.zip` in this repo.
Find the detailed instructions at https://localstack.cloud/dev-contest

## Build the lambda yourself

To build the lambda yourself, you need to create a zip file with all the necessary resources:

* the `handler.py`
* all necessary libraries
* the certificate template

If you have `pip` available globally, you can simply run

```bash
make lambda
```

Or, if you prefer to build the lambda manually:

```bash
mkdir -p build
pip install -r requirements.txt -t build/
rm -f demo-lambda.zip
zip demo-lambda.zip handler.py cert_template.pdf
(cd build; zip ../demo-lambda.zip -r .)
```

Now, use the `demo-lambda.zip` as described in the contest instructions!
