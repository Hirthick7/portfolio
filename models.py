from pymongo import MongoClient
from datetime import datetime
from config import Config

class Database:
    """MongoDB database connection handler"""
    
    _client = None
    _db = None
    
    @classmethod
    def get_db(cls):
        """Get database instance (singleton pattern)"""
        if cls._db is None:
            cls._client = MongoClient(Config.MONGO_URI)
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
        """
        Create a new contact message
        
        Args:
            name (str): Sender's name
            email (str): Sender's email
            message (str): Message content
            
        Returns:
            dict: Inserted document with _id
        """
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
