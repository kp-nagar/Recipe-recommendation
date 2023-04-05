FROM python:3.8

WORKDIR /Recipe-recommendation

COPY requirements.txt /Recipe-recommendation/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /Recipe-recommendation/requirements.txt

COPY . /Recipe-recommendation

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
