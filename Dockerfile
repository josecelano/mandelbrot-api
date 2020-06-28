FROM josecelano/mandelbrot:latest

# Install python and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    pnmtopng \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -U setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

# Install dependencies
RUN python3 -m pip install -U -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]

EXPOSE 80