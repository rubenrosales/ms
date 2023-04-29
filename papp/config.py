import os
import json
import yaml
from typing import Optional

class ConfigReader:
    """Reads configuration files in either JSON or YAML format."""
    
    def __init__(self, filename: str, directory: Optional[str] = None):
        self.filename = filename
        self.directory = directory or os.getcwd()
        self.config = None
        
    def read(self):
        file_path = os.path.join(self.directory, self.filename)
        if self.filename.endswith('.json'):
            self._read_json(file_path)
        elif self.filename.endswith('.yaml') or self.filename.endswith('.yml'):
            self._read_yaml(file_path)
        else:
            raise ValueError('Unsupported configuration file type.')
    
    def _read_json(self, file_path: str):
        with open(file_path, 'r') as f:
            self.config = json.load(f)
            
    def _read_yaml(self, file_path: str):
        with open(file_path, 'r') as f:
            self.config = yaml.safe_load(f)
