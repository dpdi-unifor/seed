# -*- coding: utf-8 -*-
import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, \
    Enum, DateTime, Numeric, Text, Unicode, UnicodeText
from sqlalchemy import event
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_i18n import make_translatable, translation_base, Translatable

make_translatable(options={'locales': ['pt', 'en'],
                           'auto_create_locales': True,
                           'fallback_locale': 'en'})

db = SQLAlchemy()


# noinspection PyClassHasNoInit
class DeploymentType:
    DOCKER = 'DOCKER'
    SUPERVISOR = 'SUPERVISOR'
    MARATHON = 'MARATHON'
    KUBERNETES = 'KUBERNETES'

    @staticmethod
    def values():
        return [n for n in DeploymentType.__dict__.keys()
                if n[0] != '_' and n != 'values']


# noinspection PyClassHasNoInit
class DeploymentStatus:
    STOPPED = 'STOPPED'
    RUNNING = 'RUNNING'
    EDITING = 'EDITING'
    SAVED = 'SAVED'
    SUSPENDED = 'SUSPENDED'

    @staticmethod
    def values():
        return [n for n in DeploymentStatus.__dict__.keys()
                if n[0] != '_' and n != 'values']


class Client(db.Model):
    """ Service client configuration """
    __tablename__ = 'client'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    enabled = Column(Boolean, nullable=False)
    token = Column(String(256), nullable=False)

    # Associations
    deployment_id = Column(Integer,
                           ForeignKey("deployment.id"), nullable=False)
    deployment = relationship(
        "Deployment",
        foreign_keys=[deployment_id])

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)


class Deployment(db.Model):
    """ Deployment """
    __tablename__ = 'deployment'

    # Fields
    id = Column(Integer, primary_key=True)
    description = Column(String(400))
    created = Column(DateTime,
                     default=func.now(), nullable=False)
    updated = Column(DateTime,
                     default=func.now(), nullable=False,
                     onupdate=datetime.datetime.utcnow)
    command = Column(String(5000))
    workflow_name = Column(String(200), nullable=False)
    workflow_id = Column(Integer, nullable=False)
    job_id = Column(Integer)
    user_id = Column(Integer, nullable=False)
    user_login = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=False)
    enabled = Column(Boolean,
                     default=False, nullable=False)
    current_status = Column(Enum(*DeploymentStatus.values(),
                                 name='DeploymentStatusEnumType'),
                            default=DeploymentStatus.EDITING, nullable=False)
    attempts = Column(Integer,
                      default=0, nullable=False)
    log = Column(String(16000000))
    entry_point = Column(String(800))

    # Associations
    target_id = Column(Integer,
                       ForeignKey("deployment_target.id"))
    target = relationship(
        "DeploymentTarget",
        foreign_keys=[target_id])
    image_id = Column(Integer,
                      ForeignKey("deployment_image.id"))
    image = relationship(
        "DeploymentImage",
        foreign_keys=[image_id])

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)


class DeploymentImage(db.Model):
    """ Deployment image """
    __tablename__ = 'deployment_image'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    tag = Column(String(100), nullable=False)
    enabled = Column(Boolean, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)


class DeploymentLog(db.Model):
    """ Logs for deployment """
    __tablename__ = 'deployment_log'

    # Fields
    id = Column(Integer, primary_key=True)
    date = Column(DateTime,
                  default=datetime.datetime.utcnow, nullable=False)
    status = Column(Enum(*DeploymentStatus.values(),
                         name='DeploymentStatusEnumType'), nullable=False)
    log = Column(String(16000000), nullable=False)

    # Associations
    deployment_id = Column(Integer,
                           ForeignKey("deployment.id"), nullable=False)
    deployment = relationship(
        "Deployment",
        foreign_keys=[deployment_id])

    def __unicode__(self):
        return self.date

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)


class DeploymentMetric(db.Model):
    """ Metrics for deployment """
    __tablename__ = 'deployment_metric'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    parameters = Column(String(1000), nullable=False)
    enabled = Column(Boolean, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_login = Column(String(100), nullable=False)

    # Associations
    deployment_id = Column(Integer,
                           ForeignKey("deployment.id"), nullable=False)
    deployment = relationship(
        "Deployment",
        foreign_keys=[deployment_id])

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)


class DeploymentTarget(db.Model):
    """ Deployment target """
    __tablename__ = 'deployment_target'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(400))
    url = Column(String(500), nullable=False)
    authentication_info = Column(String(500))
    enabled = Column(Boolean, nullable=False)
    target_type = Column(Enum(*DeploymentType.values(),
                              name='DeploymentTypeEnumType'), nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Instance {}: {}>'.format(self.__class__, self.id)

