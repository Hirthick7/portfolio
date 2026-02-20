from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from config import Config

class Database:
    """MongoDB database connection handler"""
    
    _client = None
    _db = None
    
    @classmethod
    def get_db(cls):
        """Get database instance (singleton pattern)"""
        if cls._db is None:
            cls._client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
            cls._db = cls._client[Config.MONGO_DB_NAME]
        return cls._db
    
    @classmethod
    def close(cls):
        """Close database connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None


class ContactMessage:
    """Contact form message model"""
    
    collection_name = 'resume'
    
    @staticmethod
    def create(name, email, message):
        db = Database.get_db()
        collection = db[ContactMessage.collection_name]
        document = {
            'name': name,
            'email': email,
            'message': message,
            'created_at': datetime.utcnow(),
            'read': False
        }
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        return document
    
    @staticmethod
    def get_all():
        """Get all contact messages"""
        db = Database.get_db()
        collection = db[ContactMessage.collection_name]
        return list(collection.find().sort('created_at', -1))
    
    @staticmethod
    def mark_as_read(message_id):
        """Mark a message as read"""
        db = Database.get_db()
        collection = db[ContactMessage.collection_name]
        collection.update_one(
            {'_id': message_id},
            {'$set': {'read': True}}
        )


class Skill:
    """Dynamic skill model for admin-managed skills"""
    
    collection_name = 'skills'
    
    @staticmethod
    def create(name, category, proficiency):
        """
        Create a new skill entry.
        
        Args:
            name (str): Skill name (e.g. 'React')
            category (str): Category label (e.g. 'Web Development')
            proficiency (int): Proficiency percentage 0-100
        """
        db = Database.get_db()
        collection = db[Skill.collection_name]
        document = {
            'name': name,
            'category': category,
            'proficiency': int(proficiency),
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        return document
    
    @staticmethod
    def get_all():
        """Get all skills sorted by category then name"""
        db = Database.get_db()
        collection = db[Skill.collection_name]
        return list(collection.find().sort([('category', 1), ('name', 1)]))
    
    @staticmethod
    def get_by_id(skill_id):
        """Get a skill by its ObjectId string"""
        db = Database.get_db()
        collection = db[Skill.collection_name]
        return collection.find_one({'_id': ObjectId(skill_id)})

    @staticmethod
    def update(skill_id, name, category, proficiency):
        """Update a skill by its ObjectId string"""
        db = Database.get_db()
        collection = db[Skill.collection_name]
        collection.update_one(
            {'_id': ObjectId(skill_id)},
            {
                '$set': {
                    'name': name,
                    'category': category,
                    'proficiency': int(proficiency)
                }
            }
        )

    @staticmethod
    def delete(skill_id):
        """Delete a skill by its ObjectId string"""
        db = Database.get_db()
        collection = db[Skill.collection_name]
        collection.delete_one({'_id': ObjectId(skill_id)})


class Certificate:
    """Certificate model for admin-managed certificates"""
    
    collection_name = 'certificates'
    
    @staticmethod
    def create(title, issuer, issue_date, credential_url, description):
        """
        Create a new certificate entry.
        
        Args:
            title (str): Certificate title
            issuer (str): Issuing organisation
            issue_date (str): Date string (e.g. 'Jan 2025')
            credential_url (str): URL to verify the credential (optional)
            description (str): Short description (optional)
        """
        db = Database.get_db()
        collection = db[Certificate.collection_name]
        document = {
            'title': title,
            'issuer': issuer,
            'issue_date': issue_date,
            'credential_url': credential_url,
            'description': description,
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        return document
    
    @staticmethod
    def get_all():
        """Get all certificates sorted newest first"""
        db = Database.get_db()
        collection = db[Certificate.collection_name]
        return list(collection.find().sort('created_at', -1))
    
    @staticmethod
    def get_by_id(cert_id):
        """Get a certificate by its ObjectId string"""
        db = Database.get_db()
        collection = db[Certificate.collection_name]
        return collection.find_one({'_id': ObjectId(cert_id)})

    @staticmethod
    def update(cert_id, title, issuer, issue_date, credential_url, description):
        """Update a certificate by its ObjectId string"""
        db = Database.get_db()
        collection = db[Certificate.collection_name]
        collection.update_one(
            {'_id': ObjectId(cert_id)},
            {
                '$set': {
                    'title': title,
                    'issuer': issuer,
                    'issue_date': issue_date,
                    'credential_url': credential_url,
                    'description': description
                }
            }
        )

    @staticmethod
    def delete(cert_id):
        """Delete a certificate by its ObjectId string"""
        db = Database.get_db()
        collection = db[Certificate.collection_name]
        collection.delete_one({'_id': ObjectId(cert_id)})


class Project:
    """Project model for admin-managed projects"""

    collection_name = 'projects'

    @staticmethod
    def create(title, description, tags, github_url, live_url, icon):
        db = Database.get_db()
        collection = db[Project.collection_name]
        document = {
            'title': title,
            'description': description,
            'tags': [t.strip() for t in tags.split(',') if t.strip()],
            'github_url': github_url,
            'live_url': live_url,
            'icon': icon or 'fa-code',
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        return document

    @staticmethod
    def get_all():
        """Get all projects sorted newest first"""
        db = Database.get_db()
        collection = db[Project.collection_name]
        return list(collection.find().sort('created_at', -1))

    @staticmethod
    def get_by_id(project_id):
        """Get a project by its ObjectId string"""
        db = Database.get_db()
        collection = db[Project.collection_name]
        return collection.find_one({'_id': ObjectId(project_id)})

    @staticmethod
    def update(project_id, title, description, tags, github_url, live_url, icon):
        """Update a project by its ObjectId string"""
        db = Database.get_db()
        collection = db[Project.collection_name]
        collection.update_one(
            {'_id': ObjectId(project_id)},
            {
                '$set': {
                    'title': title,
                    'description': description,
                    'tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'github_url': github_url,
                    'live_url': live_url,
                    'icon': icon or 'fa-code'
                }
            }
        )

    @staticmethod
    def delete(project_id):
        """Delete a project by its ObjectId string"""
        db = Database.get_db()
        collection = db[Project.collection_name]
        collection.delete_one({'_id': ObjectId(project_id)})

