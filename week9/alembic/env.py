# alembic/env.py 상단 수정 예시
# ... 기존 코드 ...
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 프로젝트 경로를 인식시키기 위한 코드
sys.path.append(os.getcwd())
from models import Base # models.py의 Base를 임포트

# ... 기존 코드 ...
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata # 이 부분을 수정