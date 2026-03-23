from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session, scoped_session

Base = declarative_base()

# --- Models ---

class OntologyVersion(Base):
    __tablename__ = 'ontology_versions'

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    description = Column(String)

    nodes = relationship("OntologyNode", back_populates="version", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "tag": self.tag, "created_at": self.created_at, "description": self.description}

class OntologyNode(Base):
    __tablename__ = 'ontology_nodes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    metadata_json = Column(JSON, default={})
    version_id = Column(Integer, ForeignKey('ontology_versions.id'), nullable=False)

    version = relationship("OntologyVersion", back_populates="nodes")
    children_edges = relationship("OntologyEdge", foreign_keys="[OntologyEdge.parent_id]", back_populates="parent", cascade="all, delete-orphan")
    parent_edges = relationship("OntologyEdge", foreign_keys="[OntologyEdge.child_id]", back_populates="child", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "metadata": self.metadata_json, "version_id": self.version_id}

class OntologyEdge(Base):
    __tablename__ = 'ontology_edges'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('ontology_nodes.id'), nullable=False)
    child_id = Column(Integer, ForeignKey('ontology_nodes.id'), nullable=False)
    weight = Column(Float, default=1.0)
    type = Column(String, nullable=False)

    parent = relationship("OntologyNode", foreign_keys=[parent_id], back_populates="children_edges")
    child = relationship("OntologyNode", foreign_keys=[child_id], back_populates="parent_edges")

    def to_dict(self):
        return {"id": self.id, "parent_id": self.parent_id, "child_id": self.child_id, "weight": self.weight, "type": self.type}

class ChangeLog(Base):
    __tablename__ = 'change_logs'

    id = Column(Integer, primary_key=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    details = Column(JSON)

    def to_dict(self):
        return {"id": self.id, "entity": self.entity_type, "action": self.action, "timestamp": self.timestamp, "details": self.details}

# --- Abstraction ---

class IDataLoader(ABC):
    @abstractmethod
    def load_data(self) -> List[Dict[str, Any]]:
        pass

# --- Engine ---

class OntologyEngine:
    def __init__(self, db_url="sqlite:///ontology.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self._current_version_id = None

    def _log_change(self, session, entity_type, entity_id, action, details=None):
        log = ChangeLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            details=details
        )
        session.add(log)

    def set_version(self, tag, description=None):
        session = self.Session()
        try:
            version = session.query(OntologyVersion).filter_by(tag=tag).first()
            if not version:
                version = OntologyVersion(tag=tag, description=description)
                session.add(version)
                session.flush()
                self._log_change(session, 'OntologyVersion', version.id, 'INSERT', {'tag': tag})
                session.commit()
            self._current_version_id = version.id
            return version.to_dict()
        finally:
            self.Session.remove()

    def create_node(self, name, metadata=None):
        if not self._current_version_id:
            raise ValueError("No active version set. Use set_version() first.")

        session = self.Session()
        try:
            node = OntologyNode(
                name=name,
                metadata_json=metadata or {},
                version_id=self._current_version_id
            )
            session.add(node)
            session.flush()
            self._log_change(session, 'OntologyNode', node.id, 'INSERT', {'name': name})
            session.commit()
            return node.id
        finally:
            self.Session.remove()

    def create_relationship(self, parent_id, child_id, rel_type, weight=1.0):
        session = self.Session()
        try:
            edge = OntologyEdge(
                parent_id=parent_id,
                child_id=child_id,
                type=rel_type,
                weight=weight
            )
            session.add(edge)
            session.flush()
            self._log_change(session, 'OntologyEdge', edge.id, 'INSERT', {
                'parent_id': parent_id,
                'child_id': child_id,
                'type': rel_type,
                'weight': weight
            })
            session.commit()
            return edge.id
        finally:
            self.Session.remove()

    def get_node(self, node_id):
        session = self.Session()
        try:
            node = session.query(OntologyNode).filter_by(id=node_id).first()
            return node.to_dict() if node else None
        finally:
            self.Session.remove()

    def get_version_nodes(self, version_tag):
        session = self.Session()
        try:
            version = session.query(OntologyVersion).filter_by(tag=version_tag).first()
            if version:
                nodes = session.query(OntologyNode).filter_by(version_id=version.id).all()
                return [n.to_dict() for n in nodes]
            return []
        finally:
            self.Session.remove()

    def get_logs(self, limit=50):
        session = self.Session()
        try:
            logs = session.query(ChangeLog).order_by(ChangeLog.timestamp.desc()).limit(limit).all()
            return [log.to_dict() for log in logs]
        finally:
            self.Session.remove()

    def bulk_load(self, loader: IDataLoader):
        """Higher-level abstraction for data loading."""
        data = loader.load_data()
        results = []
        for item in data:
            # Simple example: if 'parent_name' and 'child_name' exists, we create nodes and relations.
            # This logic should be more robust based on the implementation of the loader.
            pass
        return results
