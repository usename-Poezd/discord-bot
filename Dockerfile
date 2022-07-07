FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

COPY . /code

CMD [ "python", "bot.py" ]