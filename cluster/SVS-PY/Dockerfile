FROM python:3.11

RUN apt update && \
    apt install -y libleveldb-dev 

COPY ndn-python-svs /ndn-python-svs
RUN pip install -r /ndn-python-svs/docs/requirements.txt

RUN cd /ndn-python-svs && python -c "from ndn.security.keychain.keychain_sqlite3 import KeychainSqlite3; KeychainSqlite3.initialize('./pib.db', 'tpm-file')"

