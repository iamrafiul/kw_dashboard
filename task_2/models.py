from app import db


# Model class for the table "device_health"
class DeviceHealth(db.Model):
    __tablename__ = 'device_health'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)

    device_id = db.Column(db.String(20), nullable=False)
    device_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime())

    def __init__(self, device_id, device_type, status, date_created):
        self.device_id = device_id
        self.device_type = device_type
        self.status = status
        self.date_created = date_created

    def __repr__(self):
        return '<id {}>'.format(self.device_id)
