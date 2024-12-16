
FROM python:3.12.3


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip


RUN pip install --retries 5 --timeout 300 --no-cache-dir --upgrade  -r /code/requirements.txt

RUN pip install "fastapi[standard]"


COPY . /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "9000"]