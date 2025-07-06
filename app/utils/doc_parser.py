from uuid import uuid4

def parse_document_input(title: str, content: str) -> dict:
    """
    Parses raw title and content into a document dict with a unique ID.

    Args:
        title (str): Document title (can be empty or None).
        content (str): The main document text content.

    Returns:
        dict: A clean document with fields: doc_id, title, content

    Raises:
        ValueError: If content is empty after stripping.
    """
    if not content or not content.strip():
        raise ValueError("Document content cannot be empty.")

    return {
        "doc_id": str(uuid4()),
        "title": title.strip() if title else "Untitled Document",
        "content": content.strip()
    }
