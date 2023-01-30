FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install .
CMD ["python", "legal_copilot/main.py", "--host", "0.0.0.0", "--port", "5000"]