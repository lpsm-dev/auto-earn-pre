FROM python:3.10.4-alpine3.14 as base

FROM base as install
WORKDIR /tmp
COPY ["requirements.txt", "."]
RUN set -ex && \
    pip install --no-cache-dir \
      --no-warn-script-location \
      --user -r requirements.txt

FROM base
COPY --from=install ["/root/.local", "/usr/local"]
WORKDIR /usr/src/code
COPY ["src/", "."]
RUN set -ex && \
    find ./ -iname "*.py" -type f -exec chmod a+x {} \; -exec echo {} \;

CMD ["python", "main.py"]
