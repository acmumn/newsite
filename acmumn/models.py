from acmumn.globals import db

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    x500 = db.Column(db.String, unique=True)
    student_id = db.Column(db.Integer, unique=True)
    discord_id = db.Column(db.Integer, unique=True)

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), nullable=False)
    location = db.Column(db.Unicode(256))
    description = db.Column(db.Text)

attendance = db.Table("attendance",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id", nullable=False)),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id", nullable=False)),
    db.PrimaryKeyConstraint("member_id", "event_id"))

class MailingList(db.Model):
    __tablename__ = "mailing_lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)

subscriptions = db.Table("subscriptions",
    db.Column("member_id", db.Integer, db.ForeignKey("members.id", nullable=False)),
    db.Column("list_id", db.Integer, db.ForeignKey("mailing_lists.id", nullable=False)),
    db.PrimaryKeyConstraint("member_id", "list_id"))
