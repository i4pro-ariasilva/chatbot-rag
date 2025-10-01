import os
import logging
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup
from PIL import Image
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processes HTML documents and images from the specified directory."""
    
    def __init__(self):
        self.documents_dir = Path(config.DOCUMENTS_DIR)
        if not self.documents_dir.exists():
            logger.error(f"Documents directory does not exist: {self.documents_dir}")
            raise FileNotFoundError(f"Directory not found: {self.documents_dir}")
    
    def scan_documents(self) -> List[Path]:
        """Scan the documents directory for HTML, text and image files."""
        logger.info(f"Scanning directory: {self.documents_dir}")
        
        files = []
        # HTML files
        for ext in config.SUPPORTED_HTML_EXTENSIONS:
            files.extend(self.documents_dir.glob(f"**/*{ext}"))
        
        # Text files
        for ext in config.SUPPORTED_TEXT_EXTENSIONS:
            files.extend(self.documents_dir.glob(f"**/*{ext}"))
        
        html_count = sum(1 for f in files if f.suffix.lower() in [ext.lower() for ext in config.SUPPORTED_HTML_EXTENSIONS])
        txt_count = sum(1 for f in files if f.suffix.lower() in [ext.lower() for ext in config.SUPPORTED_TEXT_EXTENSIONS])
        
        logger.info(f"Found {html_count} HTML documents and {txt_count} text documents")
        return files
    
    def process_html_file(self, file_path: Path) -> dict:
        """Extract text content from HTML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'content': text,
                'content_type': 'html',
                'title': soup.title.string if soup.title else file_path.stem
            }
            
        except Exception as e:
            logger.error(f"Error processing HTML file {file_path}: {e}")
            return None
    
    def process_text_file(self, file_path: Path) -> dict:
        """Extract text content from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Clean up text (remove excessive whitespace)
            lines = (line.strip() for line in content.splitlines())
            text = '\n'.join(line for line in lines if line)
            
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'content': text,
                'content_type': 'text',
                'title': file_path.stem
            }
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return None
    
    def simple_image_processing(self, file_path: Path) -> Optional[dict]:
        """Simple image processing without OCR - just metadata."""
        try:
            # Open image to get basic info
            with Image.open(file_path) as image:
                width, height = image.size
                format_type = image.format
            
            # Create basic description based on filename and size
            description = f"Imagem {file_path.stem} ({width}x{height} {format_type})"
            
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'content': description,
                'content_type': 'image',
                'title': file_path.stem
            }
            
        except Exception as e:
            logger.error(f"Error processing image file {file_path}: {e}")
            return None
    
    def process_all_documents(self) -> List[dict]:
        """Process all documents in the directory."""
        files = self.scan_documents()
        processed_docs = []
        
        for file_path in files:
            logger.info(f"Processing: {file_path.name}")
            
            if file_path.suffix.lower() in config.SUPPORTED_HTML_EXTENSIONS:
                doc = self.process_html_file(file_path)
                if doc:
                    processed_docs.append(doc)
            elif file_path.suffix.lower() in config.SUPPORTED_TEXT_EXTENSIONS:
                doc = self.process_text_file(file_path)
                if doc:
                    processed_docs.append(doc)
        
        # Adicionar imagens com processamento básico
        image_files = []
        for ext in config.SUPPORTED_IMAGE_EXTENSIONS:
            image_files.extend(self.documents_dir.glob(f"**/*{ext}"))
        
        for file_path in image_files[:10]:  # Limitar a 10 imagens para não sobrecarregar
            doc = self.simple_image_processing(file_path)
            if doc:
                processed_docs.append(doc)
        
        logger.info(f"Successfully processed {len(processed_docs)} documents")
        return processed_docs
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into chunks for better processing."""
        chunk_size = chunk_size or config.CHUNK_SIZE
        overlap = overlap or config.CHUNK_OVERLAP
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence end
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start + chunk_size // 2, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunks.append(text[start:end].strip())
            start = end - overlap
        
        return [chunk for chunk in chunks if chunk.strip()]