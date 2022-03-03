FROM  python:3.10 
COPY ./requirements.txt .


RUN pip install -r ./requirements.txt

COPY . .

CMD ["python", "./server.py"]