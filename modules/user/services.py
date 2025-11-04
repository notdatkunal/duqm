from typing import Type

import pandas as pd
from fob_postgres.tables import FobUsers, FobUserRole, FobInternalCustomerUser
from fob_postgres.pg_session import postgres_session
from datetime import datetime
from sqlalchemy import update,and_
from helpers.commonn_utils import model_to_dict
from helpers.exceptions import BadRequestException


def user_list_service():
    query = postgres_session.get_session().query(
        FobUsers,
        FobUserRole.role_name,
        FobUserRole.date_time_closed,
    ).join(
        FobUserRole, FobUsers.login_id == FobUserRole.login_id
    ).order_by(FobUsers.date_time_joined.desc())

    result = pd.read_sql(query.statement,query.session.bind)
    result["date_time_closed"] = result["date_time_closed"].astype(str).replace("NaT", "")
    result["date_time_closed"] = result["date_time_closed"].astype(str).replace("None", "")
    result = result.to_dict(orient="records")
    return result


def create_user_service(data:dict):
    sess = postgres_session.get_session()
    logo_count = 0
    if data["role_name"] == "LOGO":
        logo_count = sess.query(FobUserRole).filter(and_(
            FobUserRole.role_name == "LOGO",
            FobUserRole.date_time_closed.is_(None)
        )).count()
    if logo_count == 2:
        raise BadRequestException("Only 2 users with role LOGO allowed")
    # check if user already exist
    exist_user = sess.query(FobUsers.login_id).filter(
        FobUsers.login_id==data["login_id"]
    ).first()
    if exist_user is None:
        user_model = FobUsers(
            login_id = data["login_id"],
            id=data["id"],
            name=data["name"],
            rank = data['rank'],
            department = data['department'],
            date_time_joined = datetime.now(),
            station_code=data["station_code"],
        )
        sess.add(user_model)
        sess.flush()
    user_role_model =FobUserRole(
        login_id = data["login_id"],
        role_name=data["role_name"],
        date_time_activated = datetime.now(),
        station_code = data["station_code"],
    )
    customer_user_model = FobInternalCustomerUser(
        login_id = data['login_id'],
        role_name = data["role_name"],
        customer_code = data["customer_code"],
        date_time_added = datetime.now(),
        added_by = data["added_by"],
    )
    
    
    sess.add(user_role_model)
    sess.flush()
    sess.add(customer_user_model)
    sess.commit()
    return True


def close_user_service(login_id:str, role_name:str):
    with (postgres_session.get_session() as sess):
        user_obj: Type[FobUserRole] = (sess.query(FobUserRole).filter(
            FobUserRole.login_id.startswith(login_id.strip()) ,
            FobUserRole.role_name.startswith(role_name.strip())).one())

        user_obj.date_time_closed = datetime.now()
        sess.add(user_obj)
        sess.commit()
        return True
