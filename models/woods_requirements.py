# requirements id and wood db id relations new table
from db import db


class WoodsRequirementsFromDashboardModel(db.Model):
    __tablename__ = 'woods_requirements_dashboard'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wood_id = db.Column(db.Integer, db.ForeignKey('residual_wood.id'))
    dashboard_requirement_id = db.Column(db.Integer, db.ForeignKey('requirements_from_dashboard.id'))


class WoodRequirementsFromGHModel(db.Model):
    __tablename__ = "woods_requirements_gh"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wood_id = db.Column(db.Integer, db.ForeignKey('residual_wood.id'))
    gh_requirement_id = db.Column(db.Integer, db.ForeignKey('requirements_from_grasshopper.id'))

