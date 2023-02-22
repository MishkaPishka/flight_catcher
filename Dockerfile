# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . code
WORKDIR /code

EXPOSE 8000
ENTRYPOINT ["python", "main.py"]
CMD ["emptydb.csv", "0.0.0.0:5000"]