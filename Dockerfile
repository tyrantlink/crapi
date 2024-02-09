FROM python:3.11

RUN groupadd -g 1000 -o crapi
RUN useradd -m -u 1000 -g 1000 -o -s /bin/bash crapi
USER crapi

ENV PATH /home/crapi/.local/bin:$PATH

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -U -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--forwarded-allow-ips", "*"]