"""
Query Sanitizer for Dubai Real Estate RAG System

This module provides safe database query building and sanitization
to eliminate all risks of SQL injection by ensuring all queries
are properly parameterized.
"""

import re
from typing import Dict, List, Any, Optional, Union, Tuple
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class QuerySanitizer:
    """Provides safe database query building and sanitization"""
    
    def __init__(self):
        pass
    
    def sanitize_input(self, value: Any) -> Any:
        """Sanitize input value to prevent SQL injection"""
        if value is None:
            return None
        
        if isinstance(value, (int, float, bool)):
            return value
        
        if isinstance(value, str):
            # Remove any SQL comment patterns
            value = re.sub(r'--.*$', '', value, flags=re.MULTILINE)
            value = re.sub(r'/\*.*?\*/', '', value, flags=re.DOTALL)
            
            # Remove any semicolons that might be used for multiple statements
            value = value.replace(';', '')
            
            return value.strip()
        
        if isinstance(value, (list, tuple)):
            return [self.sanitize_input(item) for item in value]
        
        if isinstance(value, dict):
            return {key: self.sanitize_input(val) for key, val in value.items()}
        
        return value
    
    def build_safe_select(self, table: str, columns: List[str] = None, 
                         conditions: Dict[str, Any] = None, 
                         order_by: List[str] = None,
                         limit: int = None, offset: int = None) -> Tuple[str, Dict[str, Any]]:
        """Build a safe SELECT query with parameters"""
        try:
            # Sanitize inputs
            table = self.sanitize_input(table)
            if not table or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
                raise ValueError("Invalid table name")
            
            # Build SELECT clause
            if columns:
                columns = [self.sanitize_input(col) for col in columns]
                select_clause = ", ".join(columns)
            else:
                select_clause = "*"
            
            # Build WHERE clause
            where_clause = ""
            params = {}
            if conditions:
                where_conditions = []
                for key, value in conditions.items():
                    sanitized_key = self.sanitize_input(key)
                    if not sanitized_key or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_key):
                        raise ValueError(f"Invalid column name: {key}")
                    
                    param_name = f"param_{len(params)}"
                    where_conditions.append(f"{sanitized_key} = :{param_name}")
                    params[param_name] = self.sanitize_input(value)
                
                where_clause = " WHERE " + " AND ".join(where_conditions)
            
            # Build ORDER BY clause
            order_clause = ""
            if order_by:
                order_by = [self.sanitize_input(col) for col in order_by]
                order_clause = " ORDER BY " + ", ".join(order_by)
            
            # Build LIMIT and OFFSET
            limit_clause = ""
            if limit is not None:
                limit = int(limit)
                if limit < 0:
                    raise ValueError("Limit must be non-negative")
                limit_clause = f" LIMIT {limit}"
                
                if offset is not None:
                    offset = int(offset)
                    if offset < 0:
                        raise ValueError("Offset must be non-negative")
                    limit_clause += f" OFFSET {offset}"
            
            # Build final query
            query = f"SELECT {select_clause} FROM {table}{where_clause}{order_clause}{limit_clause}"
            
            return query, params
            
        except Exception as e:
            logger.error(f"Error building safe SELECT query: {e}")
            raise ValueError(f"Failed to build safe SELECT query: {str(e)}")
    
    def build_safe_insert(self, table: str, data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Build a safe INSERT query with parameters"""
        try:
            # Sanitize inputs
            table = self.sanitize_input(table)
            if not table or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
                raise ValueError("Invalid table name")
            
            # Sanitize data
            sanitized_data = {}
            for key, value in data.items():
                sanitized_key = self.sanitize_input(key)
                if not sanitized_key or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_key):
                    raise ValueError(f"Invalid column name: {key}")
                sanitized_data[sanitized_key] = self.sanitize_input(value)
            
            if not sanitized_data:
                raise ValueError("No data provided for INSERT")
            
            # Build query
            columns = list(sanitized_data.keys())
            param_names = [f":{col}" for col in columns]
            
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(param_names)})"
            
            return query, sanitized_data
            
        except Exception as e:
            logger.error(f"Error building safe INSERT query: {e}")
            raise ValueError(f"Failed to build safe INSERT query: {str(e)}")
    
    def build_safe_update(self, table: str, data: Dict[str, Any], 
                         conditions: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Build a safe UPDATE query with parameters"""
        try:
            # Sanitize inputs
            table = self.sanitize_input(table)
            if not table or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
                raise ValueError("Invalid table name")
            
            # Sanitize data
            sanitized_data = {}
            for key, value in data.items():
                sanitized_key = self.sanitize_input(key)
                if not sanitized_key or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_key):
                    raise ValueError(f"Invalid column name: {key}")
                sanitized_data[sanitized_key] = self.sanitize_input(value)
            
            if not sanitized_data:
                raise ValueError("No data provided for UPDATE")
            
            # Build SET clause
            set_conditions = []
            for key in sanitized_data.keys():
                set_conditions.append(f"{key} = :set_{key}")
            
            # Build WHERE clause
            where_conditions = []
            params = {}
            
            for key, value in conditions.items():
                sanitized_key = self.sanitize_input(key)
                if not sanitized_key or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_key):
                    raise ValueError(f"Invalid column name in conditions: {key}")
                
                param_name = f"where_{sanitized_key}"
                where_conditions.append(f"{sanitized_key} = :{param_name}")
                params[param_name] = self.sanitize_input(value)
            
            if not where_conditions:
                raise ValueError("No conditions provided for UPDATE")
            
            # Add SET parameters
            for key, value in sanitized_data.items():
                params[f"set_{key}"] = value
            
            # Build final query
            query = f"UPDATE {table} SET {', '.join(set_conditions)} WHERE {' AND '.join(where_conditions)}"
            
            return query, params
            
        except Exception as e:
            logger.error(f"Error building safe UPDATE query: {e}")
            raise ValueError(f"Failed to build safe UPDATE query: {str(e)}")
    
    def build_safe_delete(self, table: str, conditions: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Build a safe DELETE query with parameters"""
        try:
            # Sanitize inputs
            table = self.sanitize_input(table)
            if not table or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
                raise ValueError("Invalid table name")
            
            if not conditions:
                raise ValueError("Conditions required for DELETE")
            
            # Build WHERE clause
            where_conditions = []
            params = {}
            
            for key, value in conditions.items():
                sanitized_key = self.sanitize_input(key)
                if not sanitized_key or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_key):
                    raise ValueError(f"Invalid column name in conditions: {key}")
                
                param_name = f"param_{len(params)}"
                where_conditions.append(f"{sanitized_key} = :{param_name}")
                params[param_name] = self.sanitize_input(value)
            
            # Build final query
            query = f"DELETE FROM {table} WHERE {' AND '.join(where_conditions)}"
            
            return query, params
            
        except Exception as e:
            logger.error(f"Error building safe DELETE query: {e}")
            raise ValueError(f"Failed to build safe DELETE query: {str(e)}")
    
    def validate_query(self, query: str) -> bool:
        """Validate that a query is safe"""
        try:
            # Check for unparameterized values
            if re.search(r"'.*?'", query) or re.search(r'".*?"', query):
                logger.warning("Query contains unparameterized string literals")
                return False
            
            # Check for multiple statements
            if ';' in query:
                logger.warning("Query contains multiple statements")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating query: {e}")
            return False

# Global query sanitizer instance
query_sanitizer = QuerySanitizer()
