import sys
import os
import re
import ast
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from typing import Annotated, Any, Dict, List
from fastapi import Query
from pydantic import BaseModel, Field
from retrieve.retrieve import index

class Item(BaseModel):
    query: str = Field(min_length=2, max_length=1000)

class CustomOutputRetriever:
    def __init__(self, index):
        self.retriever = index.as_retriever(
            similarity_top_k=50, 
        )
    
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        nodes = self.retriever.retrieve(query)
        
        def parse_node(node):
            title_match = re.search(r'Title:\s*(.+?)(?:\n|$)', node.text)
            title = title_match.group(1).strip() if title_match else None

            genres_match = re.search(r'Genres:\s*(\[.+?\])', node.text)
            try:
                genres = ast.literal_eval(genres_match.group(1)) if genres_match else []
            except:
                genres = []

            overview_match = re.search(r'Overview:\s*(.+?)(?:\n|$)', node.text, re.DOTALL)
            overview = overview_match.group(1).strip() if overview_match else None

            return {
                "title": title,
                "genres": genres,
                "overview": overview,
                "score": node.score,
                "metadata": node.metadata
            }
        
        modified_output = [
            parse_node(node)
            for node in nodes
            if self._should_include_node(node)
        ]
        
        return modified_output
    
    def _should_include_node(self, node):
        return node.score is not None and node.score >= 0.6

custom_retriever = CustomOutputRetriever(index)

def findRecommendations(data: Annotated[Item, Query()]):
    query = data.query
    response = custom_retriever.retrieve(query)
    return response