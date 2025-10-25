FROM python:3.13-slim

WORKDIR /app


COPY ./src /app/src
COPY ./config /app/config
COPY model.onnx /app/model.onnx
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "-m", "src.main"]