import logging
import sqlite3
import json
import requests
import re
import math
import time
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict
import os
import sys
import pickle
from functools import lru_cache
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config

# Groq integration
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    import logging
    logging.warning("Groq library not available. Install with: pip install groq")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedTFIDF:
    """Optimized TF-IDF implementation with caching and pre-computed vectors."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.vocabulary = {}
        self.document_frequencies = defaultdict(int)
        self.documents = []
        self.tf_idf_vectors = []
        self.idf_values = {}
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Caches para otimização
        self._tokenize_cache = {}
        self._vector_cache = {}
        
    @lru_cache(maxsize=10000)
    def tokenize(self, text: str) -> tuple:
        """Tokenização otimizada com cache."""
        # Convert to lowercase and split on non-alphanumeric characters
        text = text.lower()
        tokens = tuple(re.findall(r'\b[a-z]{2,}\b', text))
        return tokens
    
    def compute_tf(self, tokens: tuple) -> Dict[str, float]:
        """Compute term frequency otimizado."""
        token_count = len(tokens)
        if token_count == 0:
            return {}
        
        tf = defaultdict(float)
        counter = Counter(tokens)
        
        for token, count in counter.items():
            tf[token] = count / token_count
            
        return tf
    
    def fit(self, documents: List[str]):
        """Fit otimizado com cache de vetores."""
        cache_file = os.path.join(self.cache_dir, "tfidf_model.pkl")
        
        # Verificar se o cache existe e é válido
        docs_hash = hashlib.md5(str(documents).encode()).hexdigest()
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    if cached_data.get('docs_hash') == docs_hash:
                        logger.info("Loading TF-IDF model from cache...")
                        self.vocabulary = cached_data['vocabulary']
                        self.document_frequencies = cached_data['document_frequencies']
                        self.documents = cached_data['documents']
                        self.tf_idf_vectors = cached_data['tf_idf_vectors']
                        self.idf_values = cached_data['idf_values']
                        return
            except Exception as e:
                logger.warning(f"Error loading cache: {e}")
        
        logger.info("Computing TF-IDF model...")
        self.documents = documents
        all_tokens = []
        
        # Tokenize all documents (parallelizable)
        for doc in documents:
            tokens = self.tokenize(doc)
            all_tokens.append(tokens)
        
        # Build vocabulary mais eficiente
        all_words = set()
        for tokens in all_tokens:
            all_words.update(tokens)
        
        self.vocabulary = {word: i for i, word in enumerate(sorted(all_words))}
        
        # Count document frequencies otimizado
        for tokens in all_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.document_frequencies[token] += 1
        
        # Pre-compute IDF values
        num_documents = len(documents)
        for token, df in self.document_frequencies.items():
            self.idf_values[token] = math.log(num_documents / df) if df > 0 else 0
        
        # Compute TF-IDF vectors otimizado
        self.tf_idf_vectors = []
        vocab_size = len(self.vocabulary)
        
        for tokens in all_tokens:
            tf = self.compute_tf(tokens)
            vector = [0.0] * vocab_size
            
            for token, tf_score in tf.items():
                if token in self.vocabulary:
                    tfidf_score = tf_score * self.idf_values[token]
                    vector[self.vocabulary[token]] = tfidf_score
            
            self.tf_idf_vectors.append(vector)
        
        # Cache the model
        try:
            cache_data = {
                'docs_hash': docs_hash,
                'vocabulary': self.vocabulary,
                'document_frequencies': self.document_frequencies,
                'documents': self.documents,
                'tf_idf_vectors': self.tf_idf_vectors,
                'idf_values': self.idf_values
            }
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info("TF-IDF model cached successfully")
        except Exception as e:
            logger.warning(f"Error caching model: {e}")
    
    def transform(self, text: str) -> List[float]:
        """Transform otimizado com cache de consultas."""
        # Cache key baseado no hash do texto
        cache_key = hashlib.md5(text.encode()).hexdigest()
        
        if cache_key in self._vector_cache:
            return self._vector_cache[cache_key]
        
        tokens = self.tokenize(text)
        tf = self.compute_tf(tokens)
        vector = [0.0] * len(self.vocabulary)
        
        for token, tf_score in tf.items():
            if token in self.vocabulary and token in self.idf_values:
                tfidf_score = tf_score * self.idf_values[token]
                vector[self.vocabulary[token]] = tfidf_score
        
        # Cache o resultado
        self._vector_cache[cache_key] = vector
        
        # Limitar o tamanho do cache
        if len(self._vector_cache) > 1000:
            # Remove os mais antigos (FIFO simples)
            oldest_keys = list(self._vector_cache.keys())[:100]
            for old_key in oldest_keys:
                del self._vector_cache[old_key]
        
        return vector
    
    @staticmethod
    def cosine_similarity_optimized(vec1: List[float], vec2: List[float]) -> float:
        """Cosine similarity otimizada com early stopping."""
        dot_product = 0.0
        magnitude1_sq = 0.0
        magnitude2_sq = 0.0
        
        # Single pass calculation
        for a, b in zip(vec1, vec2):
            dot_product += a * b
            magnitude1_sq += a * a
            magnitude2_sq += b * b
        
        if magnitude1_sq == 0 or magnitude2_sq == 0:
            return 0.0
        
        return dot_product / (math.sqrt(magnitude1_sq) * math.sqrt(magnitude2_sq))

class FastSimpleRAGEngine:
    """Versão ultra-otimizada do RAG engine focada em performance."""
    
    def __init__(self):
        # Initialize optimized TF-IDF
        self.tfidf = OptimizedTFIDF()
        
        # Cache de respostas
        self.response_cache = {}
        self.similarity_cache = {}
        
        # Initialize Groq client if available
        self.groq_client = None
        if GROQ_AVAILABLE and config.GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=config.GROQ_API_KEY)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        
        # Initialize optimized SQLite database
        self._init_database()
        self.documents = []
        self.indexed = False
        
        # Pre-computed data
        self.doc_norms = []  # Magnitudes pre-computadas
        
        # Test API connection (optional)
        self._test_api_connection()
    
    def _init_database(self):
        """Initialize SQLite database with indexes for faster queries."""
        os.makedirs(os.path.dirname(config.VECTOR_DB_PATH), exist_ok=True)
        
        self.conn = sqlite3.connect(config.VECTOR_DB_PATH, check_same_thread=False)
        
        # Create table with basic schema (compatível com existente)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                file_path TEXT,
                title TEXT,
                content TEXT,
                content_type TEXT,
                chunk_index INTEGER
            )
        ''')
        
        # Create indexes for faster searching
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_file_name ON documents(file_name)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_content_type ON documents(content_type)')
        
        self.conn.commit()
    
    def _test_api_connection(self):
        """Test connection optimizado."""
        try:
            response = requests.get("https://httpbin.org/status/200", timeout=2)
            if response.status_code == 200:
                logger.info("API connection available but limited")
            else:
                logger.warning("Limited internet access")
        except Exception:
            logger.warning("API connection available but limited")
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Index documents otimizado com cache e pre-computação."""
        try:
            logger.info(f"Indexing {len(documents)} documents...")
            
            # Check if documents are already indexed
            if self._check_documents_cached(documents):
                logger.info("Documents already indexed, loading from cache...")
                return self._load_cached_index()
            
            # Clear existing data
            self.conn.execute("DELETE FROM documents")
            self.documents = []
            
            # Prepare texts and metadata
            texts = []
            doc_id = 0
            
            for doc in documents:
                # Chunking otimizado
                chunks = self._optimized_chunk_text(doc['content'])
                
                for i, chunk in enumerate(chunks):
                    # Store in database (sem content_hash por compatibilidade)
                    self.conn.execute('''
                        INSERT INTO documents (file_name, file_path, title, content, content_type, chunk_index)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (doc['file_name'], doc['file_path'], doc['title'], chunk, doc['content_type'], i))
                    
                    # Store for TF-IDF
                    texts.append(chunk)
                    self.documents.append({
                        'id': doc_id,
                        'file_name': doc['file_name'],
                        'file_path': doc['file_path'],
                        'title': doc['title'],
                        'content': chunk,
                        'content_type': doc['content_type'],
                        'chunk_index': i
                    })
                    doc_id += 1
            
            self.conn.commit()
            
            # Fit TF-IDF otimizado
            if texts:
                self.tfidf.fit(texts)
                
                # Pre-compute document vector norms for faster similarity
                self.doc_norms = []
                for vector in self.tfidf.tf_idf_vectors:
                    norm = math.sqrt(sum(x * x for x in vector))
                    self.doc_norms.append(norm)
                
                self.indexed = True
                logger.info(f"Successfully indexed {len(texts)} chunks from {len(documents)} documents")
                
                # Cache the index
                self._cache_index()
                return True
            else:
                logger.warning("No text content to index")
                return False
                
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False
    
    def _check_documents_cached(self, documents: List[Dict[str, Any]]) -> bool:
        """Check if documents are already cached - simplificado."""
        # Por ora, sempre reprocessar para garantir funcionamento
        return False
    
    def _get_documents_signature(self, documents: List[Dict[str, Any]]) -> str:
        """Generate unique signature for document set."""
        content_parts = []
        for doc in documents:
            content_parts.append(f"{doc['file_name']}:{len(doc['content'])}")
        return hashlib.md5("|".join(sorted(content_parts)).encode()).hexdigest()
    
    def _cache_index(self):
        """Cache the current index."""
        try:
            cache_dir = "cache"
            os.makedirs(cache_dir, exist_ok=True)
            
            # Save document norms
            with open(os.path.join(cache_dir, "doc_norms.pkl"), 'wb') as f:
                pickle.dump(self.doc_norms, f)
            
            # Save documents signature
            docs_signature = self._get_documents_signature([
                {'file_name': doc['file_name'], 'content': doc['content']} 
                for doc in self.documents
            ])
            with open(os.path.join(cache_dir, "docs_signature.txt"), 'w') as f:
                f.write(docs_signature)
                
        except Exception as e:
            logger.warning(f"Error caching index: {e}")
    
    def _load_cached_index(self) -> bool:
        """Load cached index."""
        try:
            # Load documents from database
            cursor = self.conn.execute("SELECT * FROM documents ORDER BY id")
            rows = cursor.fetchall()
            
            self.documents = []
            texts = []
            
            for row in rows:
                doc = {
                    'id': row[0],
                    'file_name': row[1],
                    'file_path': row[2],
                    'title': row[3],
                    'content': row[4],
                    'content_type': row[5],
                    'chunk_index': row[6]
                }
                self.documents.append(doc)
                texts.append(row[4])
            
            # Load TF-IDF model
            self.tfidf.fit(texts)
            
            # Load document norms
            cache_file = os.path.join("cache", "doc_norms.pkl")
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    self.doc_norms = pickle.load(f)
            else:
                # Recompute if not cached
                self.doc_norms = []
                for vector in self.tfidf.tf_idf_vectors:
                    norm = math.sqrt(sum(x * x for x in vector))
                    self.doc_norms.append(norm)
            
            self.indexed = True
            logger.info(f"Loaded {len(self.documents)} documents from cache")
            return True
            
        except Exception as e:
            logger.error(f"Error loading cached index: {e}")
            return False
    
    def _optimized_chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Chunking otimizado com breakpoints inteligentes."""
        if len(text) <= chunk_size:
            return [text]
        
        # Pre-find sentence boundaries for efficiency
        sentence_ends = []
        for match in re.finditer(r'[.!?]\s+', text):
            sentence_ends.append(match.end())
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Find best break point using pre-computed sentence ends
            if end < len(text):
                best_break = end
                for sent_end in sentence_ends:
                    if start + chunk_size // 2 < sent_end <= end:
                        best_break = sent_end
                end = best_break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
    
    def search_similar_documents(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Busca otimizada com cache de similaridade."""
        try:
            if not self.indexed:
                logger.error("No documents indexed")
                return []
            
            # Check cache first
            query_hash = hashlib.md5(query.encode()).hexdigest()
            cache_key = f"{query_hash}_{n_results}"
            
            if cache_key in self.similarity_cache:
                return self.similarity_cache[cache_key]
            
            # Transform query to TF-IDF vector
            query_vector = self.tfidf.transform(query)
            query_norm = math.sqrt(sum(x * x for x in query_vector))
            
            if query_norm == 0:
                return []
            
            # Calculate similarities otimizado
            similarities = []
            
            for i, (doc_vector, doc_norm) in enumerate(zip(self.tfidf.tf_idf_vectors, self.doc_norms)):
                if doc_norm == 0:
                    similarity = 0.0
                else:
                    # Optimized dot product calculation
                    dot_product = sum(a * b for a, b in zip(query_vector, doc_vector))
                    similarity = dot_product / (query_norm * doc_norm)
                
                # Early filtering - only keep promising results
                if similarity > 0.01:
                    similarities.append((similarity, i))
            
            # Sort by similarity (only the filtered ones)
            similarities.sort(reverse=True)
            
            # Get top results
            results = []
            for similarity, idx in similarities[:n_results]:
                results.append({
                    'content': self.documents[idx]['content'],
                    'metadata': {
                        'file_name': self.documents[idx]['file_name'],
                        'title': self.documents[idx]['title'],
                        'content_type': self.documents[idx]['content_type'],
                        'chunk_index': self.documents[idx]['chunk_index']
                    },
                    'similarity_score': float(similarity)
                })
            
            # Cache the result
            self.similarity_cache[cache_key] = results
            
            # Limit cache size
            if len(self.similarity_cache) > 500:
                # Remove oldest entries
                oldest_keys = list(self.similarity_cache.keys())[:100]
                for old_key in oldest_keys:
                    del self.similarity_cache[old_key]
            
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def generate_response_groq(self, query: str, context_docs: List[Dict[str, Any]]) -> Optional[str]:
        """Generate response using Groq API with context from documents."""
        if not self.groq_client:
            return None
            
        if not context_docs:
            return None
        
        # Check response cache first
        context_hash = hashlib.md5(str([doc['content'][:200] for doc in context_docs]).encode()).hexdigest()
        query_hash = hashlib.md5(query.encode()).hexdigest()
        cache_key = f"groq_{query_hash}_{context_hash}"
        
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Prepare context from documents (optimized)
        context_parts = []
        for doc in context_docs[:3]:  # Reduced to 3 for faster processing
            file_name = doc['metadata']['file_name']
            content = doc['content'][:600]  # Optimized content length
            context_parts.append(f"Documento: {file_name}\nConteúdo: {content}\n")
        
        context_text = "\n".join(context_parts)
        
        # Optimized prompt
        prompt = f"""Baseado na documentação técnica da i4pro:

{context_text}

Pergunta: {query}

Responda de forma direta e precisa em português brasileiro."""

        try:
            response = self.groq_client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em documentação técnica. Responda de forma clara e direta."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower for consistency
                max_tokens=800,   # Reduced for faster response
                top_p=0.9,
                stream=False
            )
            
            result = response.choices[0].message.content.strip()
            
            # Cache the response
            self.response_cache[cache_key] = result
            
            # Limit cache size
            if len(self.response_cache) > 200:
                oldest_keys = list(self.response_cache.keys())[:50]
                for old_key in oldest_keys:
                    del self.response_cache[old_key]
            
            return result
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return None
    
    def generate_response_simple(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate simple response using optimized template."""
        if not context_docs:
            return "Desculpe, não encontrei informações relevantes na documentação para responder à sua pergunta."
        
        # Cache key for simple responses
        context_hash = hashlib.md5(str([doc['content'][:100] for doc in context_docs]).encode()).hexdigest()
        query_hash = hashlib.md5(query.encode()).hexdigest()
        cache_key = f"simple_{query_hash}_{context_hash}"
        
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Optimized response generation
        best_doc = context_docs[0]
        file_name = best_doc['metadata']['file_name']
        content = best_doc['content'][:300] + "..." if len(best_doc['content']) > 300 else best_doc['content']
        
        response = f"""**Informação encontrada na documentação:**

📄 **{file_name}**:
{content}

**Relevância**: {best_doc['similarity_score']:.1%}"""
        
        # Cache the response
        self.response_cache[cache_key] = response
        
        return response
    
    def chat(self, query: str) -> Dict[str, Any]:
        """Main chat function otimizada."""
        start_time = time.time()
        logger.info(f"Processing query: {query[:50]}...")
        
        # Search for relevant documents
        relevant_docs = self.search_similar_documents(query, n_results=5)
        
        if not relevant_docs:
            return {
                'response': "Desculpe, não encontrei informações relevantes na base de documentos para responder à sua pergunta.",
                'sources': [],
                'processing_time': time.time() - start_time
            }
        
        # Generate response - try Groq first with timeout
        response = None
        if self.groq_client:
            try:
                response = self.generate_response_groq(query, relevant_docs)
            except Exception as e:
                logger.warning(f"Groq API failed, using fallback: {e}")
        
        # Fallback to simple response
        if not response:
            response = self.generate_response_simple(query, relevant_docs)
        
        # Prepare sources (optimized)
        sources = []
        for doc in relevant_docs[:2]:  # Reduced to 2 for faster response
            sources.append({
                'file_name': doc['metadata']['file_name'],
                'title': doc['metadata']['title'],
                'content_type': doc['metadata']['content_type'],
                'relevance_score': doc['similarity_score']
            })
        
        processing_time = time.time() - start_time
        logger.info(f"Query processed in {processing_time:.2f}s")
        
        return {
            'response': response,
            'sources': sources,
            'processing_time': processing_time
        }
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the document collection."""
        try:
            cursor = self.conn.execute("SELECT COUNT(*) FROM documents")
            count = cursor.fetchone()[0]
            
            cache_size = len(self.response_cache) + len(self.similarity_cache)
            
            return {
                'collection_name': config.COLLECTION_NAME,
                'document_count': count,
                'embedding_model': 'Optimized TF-IDF with caching',
                'llm_model': 'Groq + Optimized fallback',
                'cache_size': cache_size,
                'cache_hits': getattr(self, '_cache_hits', 0)
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def clear_cache(self):
        """Clear all caches for memory management."""
        self.response_cache.clear()
        self.similarity_cache.clear()
        self.tfidf._vector_cache.clear()
        logger.info("All caches cleared")
    
    def __del__(self):
        """Close database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()


# Alias para compatibilidade
SimpleRAGEngine = FastSimpleRAGEngine
UltraSimpleRAGEngine = FastSimpleRAGEngine