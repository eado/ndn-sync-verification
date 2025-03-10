FROM python:3.11

COPY python-ndn /python-ndn

RUN pip install python-ndn && python -c "from ndn.security.keychain.keychain_sqlite3 import KeychainSqlite3; KeychainSqlite3.initialize('./pib.db', 'tpm-file')" 


