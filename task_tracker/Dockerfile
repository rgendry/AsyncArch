FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY .. .

EXPOSE 8000 8000/tcp

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]