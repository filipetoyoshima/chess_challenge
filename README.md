# Chess Challenge

This is a study case with [Django](https://www.djangoproject.com/) that can do a few chess things.

# Build and Run

You can downloads all the dependencies with [pip](https://pypi.org/project/pip/). It is strongly recomended that you use a [virtual env](https://docs.python.org/3/library/venv.html) to do so. Just clone this repository, go into its root directory and:

```bash
python -m venv env # to create the env
. env/bin/activate # to activate the env
pip intall -r requirements.txt # to download dependencies
```

After you all setup, just tell Django to start the aplication:

```bash
python manage.py runserver
```

And voilá, you have the aplication running at you port `8000`.

# Features

For now, we have only one app, and you can check what it does at [its documentation](knight_move/README.md)

# Quality Assurance

## Automated Tests

At this project, we have [coverage](https://pypi.org/project/coverage/) installed, which will use Django built-in test tools and generate some reports for us.

```bash
coverage run manage.py test knight_move; coverage html
```

Note that we have two commands here. I put it all on the same line 'cause you probably will want to run both always. First part generate a `.coverage` file, that contains our test infos. To check it, you can run:

```bash
coverage report
```

But, for a much nicer way to see the results, the second part of our previous command should generate a `htmlcov/` directory, where are stored some cool reports, which you can read by simply opening the `index.html` file in your browser.

## Code Style

The code was written under the [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines. To verify if there are any code style problems, just run the following:

```bash
flake8 --exclude env/,chess_challenge/settings.py,*/migrations/
```

> You need flake8 installed to do this. It should be installed at the [setup step](#build-and-run).

If you run this command and nothing goes on, that's it! It's alright! It is supposed to show only problems at the code. No return, no problems :smile:

Note that in this command we are excluding certain files that are not that important to keep a style on.