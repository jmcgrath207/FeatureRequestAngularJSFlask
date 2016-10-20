from flask.ext.login import UserMixin

from app import  db


class Client_View(db.Model):
    """Model for the case view once the client logs in.

    :param int id: Unique id for the Case
    :param str client_id: Id used to identify the client
    :param int priority: Number used to represent the severity of case
    :param str target_date: the date the customer wants feature completed
    :param str product_area: Department this request is meant for
    :param str status: Status of the case
    :param str description: Client description of requested feature

    """
    __bind_key__ = 'Client_View'
    __tablename__ = 'Client_View'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(100))
    case_name = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.String(20))
    product_area = db.Column(db.String(20))
    status = db.Column(db.String(20))
    description = db.Column(db.Text)



class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


#roles_users = db.Table('roles_users',
#                       db.Column('user_id', db.Integer(),
#                                 db.ForeignKey('auth_user.id')),
#                       db.Column('role_id', db.Integer(),
#                                 db.ForeignKey('auth_role.id')))


class Role(Base,UserMixin):
    __tablename__ = 'auth_role'
    __bind_key__ = 'auth_role'
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))




class User(Base,UserMixin):
    """Model for the case view once the client logs in.

    :param str Client_id: Id used to identify the client
    :param int Password: password for client
    :param bool active: checks if user is active
    :param datetime last_login_at: client's last log in time
    :param datetime current_login_at: current time the user is log in
    :param str last_login_ip: ip address the client last login from
    :param str current_login_ip: ip address the client is current logged in from
    :param int login_count: time client has logged in
    :param pickletype api_key: time client has logged in


    """

    __tablename__ = 'auth_user'
    __bind_key__ = 'auth_user'
    Client_id = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    api_key = db.Column(db.PickleType)
    #roles = db.relationship('Role', secondary=roles_users,
    #                       backref=db.backref('Client_id', lazy='dynamic'))





