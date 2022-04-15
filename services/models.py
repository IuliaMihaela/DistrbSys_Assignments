from services import db


class Job(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String)
    timestamp = db.Column(db.String)
    status = db.Column(db.String)  # submitted, processing or done
    date_range = db.Column(db.String)
    assets = db.Column(db.String)  # collection of integers from 1 to 100

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "timestamp": self.timestamp,
            "status": self.status,
            "date_range": self.date_range,
            "assets": self.assets
        }

    def __repr__(self):
        return f"Job('{self.id}', '{self.username}', '{self.timestamp}', '{self.status}', '{self.date_range}', '{self.assets}')"


class Result(db.Model):
    # id = db.Column(db.String, primary_key=True)
    job_id = db.Column(db.String, db.ForeignKey('job.id'), primary_key= True )
    timestamp = db.Column(db.String)
    assets = db.Column(db.String)  # collection of pair asset number/ a real number between 0.0 and 1.0

    def serialize(self):
        return {
            "job_id": self.job_id,
            "assets": self.assets
        }

    def __repr__(self):
        return f"Job('{self.id}', '{self.job_id}', '{self.assets}')"


