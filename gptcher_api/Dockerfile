FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install .
CMD ["python", "gptcher_api/backend.py", "--host", "0.0.0.0", "--port", "5000"]