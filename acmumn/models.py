from datetime import datetime

from acmumn.globals import db

has_roles = db.Table("has_roles",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.PrimaryKeyConstraint("member_id", "role_id"))

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(256), nullable=False)
    name = db.Column(db.Unicode(256), nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    x500 = db.Column(db.String, unique=True)
    student_id = db.Column(db.Integer, unique=True)
    discord_id = db.Column(db.Integer, unique=True)
    roles = db.relationship("Role", secondary=has_roles, lazy="subquery", backref=db.backref("members", lazy=True))

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

class LoginToken(db.Model):
    __tablename__ = "login_tokens"
    code = db.Column(db.String(128), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship("Member", uselist=False, lazy=True)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

attendance = db.Table("attendance",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
    db.PrimaryKeyConstraint("member_id", "event_id"))

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), nullable=False)
    location = db.Column(db.Unicode(256))
    description = db.Column(db.Text)
    attendees = db.relationship("Member", secondary=attendance, lazy="subquery", backref=db.backref("events", lazy=True))

subscriptions = db.Table("subscriptions",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id"), primary_key=True),
    db.Column("list_id", db.Integer, db.ForeignKey("mailing_lists.id"), primary_key=True),
    db.PrimaryKeyConstraint("member_id", "list_id"))

class MailingList(db.Model):
    __tablename__ = "mailing_lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    subscribers = db.relation("Member", secondary=subscriptions, lazy="subquery", backref=db.backref("subscriptions", lazy=True))


