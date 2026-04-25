import faiss
import numpy as np
from typing import List, Dict

class ResourceVectorStore:
    def __init__(self):
        # Lazy-load: don't download the model until it's actually needed
        self._encoder = None
        self.dimension = 384 # Embedding size for MiniLM
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store = [] # Acts as our mock database for resource URLs

    @property
    def encoder(self):
        """Load the SentenceTransformer model only when first accessed."""
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer
            self._encoder = SentenceTransformer('all-MiniLM-L6-v2')
        return self._encoder
        
    def seed_initial_data(self, resources: List[Dict[str, str]]):
        """Seeds the FAISS index with learning materials (Courses, Docs, etc.)."""
        texts = [f"{r['skill_tag']} - {r['title']}" for r in resources]
        embeddings = self.encoder.encode(texts)
        
        # Add to FAISS index
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata_store.extend(resources)
        
    def retrieve_resources(self, skill_gap: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Searches the vector DB for resources matching the candidate's gap."""
        if self.index.ntotal == 0:
            return []
            
        query_vector = self.encoder.encode([skill_gap]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata_store):
                results.append(self.metadata_store[idx])
        return results

# Initialize a global instance for the backend to use
resource_db = ResourceVectorStore()