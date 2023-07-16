FROM python:3-alpine AS nnfeedfix-builder

COPY requirements.txt nnfeedfix/

ENV PYTHONDONTWRITEBYTECODE=1

RUN python -m venv --system-site-packages /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r nnfeedfix/requirements.txt

COPY nnfeedfix nnfeedfix/

FROM python:3-alpine

EXPOSE 18080/tcp

COPY --from=nnfeedfix-builder /opt/venv /opt/venv

COPY --from=nnfeedfix-builder nnfeedfix/ /nnfeedfix/nnfeedfix/

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONPATH="/nnfeedfix"

ENTRYPOINT ["python", "-m", "nnfeedfix"]
