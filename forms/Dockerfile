FROM python:3.12-slim

# No pip install step on purpose. app.py is stdlib-only, so there is no
# dependency that can fail to resolve and take the opt-in form down with it.
RUN useradd --system --uid 10001 --no-create-home forms

COPY app.py /app/app.py

USER forms
ENV PYTHONUNBUFFERED=1 PORT=8080 DATA_DIR=/data
EXPOSE 8080

CMD ["python", "/app/app.py"]
