FROM python:3.9
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN pip install -e /app
RUN pip install -e /app/gptcher_api
CMD ["python", "gptcher_api/gptcher_api/backend.py", "--host", "0.0.0.0", "--port", "5000"]
