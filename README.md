# Flask Skeleton
A simple flask skeleton to be cloned and then used for starting small flask applications easily. The HTML and CSS isn't perfect but the skeleton will allow you to get started quickly. To use, go to the directory where you'd like to start and run, `git clone https://github.com/zachchao/FlaskSkeleton`.

# Setup
Make sure you have python [installed](https://www.python.org/downloads/) and in your PATH
Install the dependencies with
`pip install -r .\requirements.txt`

# How to use
## app.py
Run this to start your local server on http://localhost:5000/. This is also where you put all routes for your application.

## /templates
This is where you put all of your html templates for doing a {% include 'template.html %} or for rendering templates in app.py.

# Deploying to Heroku
This skeleton has all the requirements to push to heroku out of the box(a free web hosting service).
1. Download heroku cli [here](https://devcenter.heroku.com/articles/git).
2. Run `heroku create <NAME>`
3. Do the normal git dance,

	`git add .`

	`git commit -am "first commit"`

	`git push`

	Then just add `git push heroku master` at the end and you will have pushed to heroku.
