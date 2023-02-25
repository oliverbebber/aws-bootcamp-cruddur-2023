FROM python:3.10-slim-buster

## ENV PORT=4567

# Inside Container
# Make a new folder insider the container
WORKDIR /backend-flask

# Outside Container > Inside Container
# Contains the libraries to install for the app to run
COPY requirements.txt requirements.txt

# Inside Container
# Install python libraries used for the app
RUN pip3 install -r requirements.txt


# Outside Container > Inside Container
# . is everything in the current directory
# 1st . - /backend-flask (outside container)
# 2nd . - /backend-flask (inside container)
COPY . .

# Set env vars
# Inside Container & remains set when container is running
ENV FLASK_ENV=development

EXPOSE ${PORT}

# Command to run flask
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]