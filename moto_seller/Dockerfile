FROM python:3.10

RUN apt-get update && \
    apt-get install -y nano vim lsof && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN echo "Installing Python dependencies" && \
    pip install -r requirements.txt && \
    echo "Python dependencies installed successfully"

RUN echo "Copying source code"

COPY . /app

RUN echo "Source code copied successfully"

RUN echo "Please, accept migrations and create superuser inside the container, using 'python manage.py create_superuser' command"

