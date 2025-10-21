FROM python:3.11-slim
# Set the working directory
WORKDIR /backend

RUN pip install poetry==1.6.1


# Install GPIO
RUN apt update && apt install gcc -y 
RUN pip install RPi.GPIO

# Install Poetry Deps
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false --local && poetry install

# Want to copy this last so it only changes 
COPY ./app ./app
