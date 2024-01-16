ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /myapp

# Install Python dependencies common way.
# RUN  --mount=type=bind,source=requirements.txt,target=requirements.txt \
  # pip install --no-cache-dir --upgrade -r requirements.txt

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/ ./app/
COPY main.py .
# CMD bash -c "while true; do sleep 1; done"

# Expose the port that the application listens on.
EXPOSE 8000
CMD ["python", "main.py"]
