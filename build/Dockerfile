ARG BASE_REPO
ARG BASE_TAG

FROM ${BASE_REPO}:${BASE_TAG}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements requirements

RUN pip install --no-cache-dir -r requirements/default.txt

COPY . .

RUN mv build/docker-entrypoint.sh docker-entrypoint.sh \
    && rm -rf build requirements /var/lib/apt/lists/*

EXPOSE 80

CMD ["sh", "./docker-entrypoint.sh"]
