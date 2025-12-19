# Flask 05: REST API
# Flask application demonstrating REST API development

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory data storage (replace with database in production)
books = [
    {
        'id': '1',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'year': 1925,
        'genre': 'Fiction',
        'isbn': '978-0743273565',
        'rating': 4.5,
        'created_at': '2024-01-15T10:00:00Z',
        'updated_at': '2024-01-15T10:00:00Z'
    },
    {
        'id': '2',
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'year': 1960,
        'genre': 'Fiction',
        'isbn': '978-0446310789',
        'rating': 4.8,
        'created_at': '2024-01-15T10:00:00Z',
        'updated_at': '2024-01-15T10:00:00Z'
    }
]

# Helper functions
def find_book(book_id):
    """Find a book by ID"""
    return next((book for book in books if book['id'] == book_id), None)

def validate_book_data(data):
    """Validate book data"""
    errors = []
    
    if not data.get('title'):
        errors.append('Title is required')
    if not data.get('author'):
        errors.append('Author is required')
    if not data.get('year'):
        errors.append('Year is required')
    elif not isinstance(data['year'], int) or data['year'] < 1800 or data['year'] > 2024:
        errors.append('Year must be a valid year between 1800 and 2024')
    
    return errors

def generate_response(data=None, message="", status_code=200, error=None):
    """Generate standardized API response"""
    response = {
        'success': status_code < 400,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if data is not None:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    return jsonify(response), status_code

# API Routes

@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with optional filtering and pagination"""
    try:
        # Query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        genre = request.args.get('genre')
        author = request.args.get('author')
        min_rating = request.args.get('min_rating')
        sort_by = request.args.get('sort_by', 'title')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Filter books
        filtered_books = books.copy()
        
        if genre:
            filtered_books = [book for book in filtered_books if book['genre'].lower() == genre.lower()]
        
        if author:
            filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]
        
        if min_rating:
            try:
                min_rating = float(min_rating)
                filtered_books = [book for book in filtered_books if book['rating'] >= min_rating]
            except ValueError:
                return generate_response(message="Invalid min_rating parameter", status_code=400)
        
        # Sort books
        reverse_sort = sort_order.lower() == 'desc'
        if sort_by == 'year':
            filtered_books.sort(key=lambda x: x['year'], reverse=reverse_sort)
        elif sort_by == 'rating':
            filtered_books.sort(key=lambda x: x['rating'], reverse=reverse_sort)
        elif sort_by == 'author':
            filtered_books.sort(key=lambda x: x['author'], reverse=reverse_sort)
        else:  # default to title
            filtered_books.sort(key=lambda x: x['title'], reverse=reverse_sort)
        
        # Pagination
        total_books = len(filtered_books)
        total_pages = (total_books + per_page - 1) // per_page
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_books = filtered_books[start_idx:end_idx]
        
        # Pagination metadata
        pagination = {
            'page': page,
            'per_page': per_page,
            'total_books': total_books,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
        
        return generate_response(
            data={
                'books': paginated_books,
                'pagination': pagination
            },
            message=f"Retrieved {len(paginated_books)} books"
        )
        
    except Exception as e:
        return generate_response(
            message="Internal server error",
            status_code=500,
            error=str(e)
        )

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = find_book(book_id)
    
    if not book:
        return generate_response(
            message="Book not found",
            status_code=404
        )
    
    return generate_response(
        data=book,
        message="Book retrieved successfully"
    )

@app.route('/api/books', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        # Check if request has JSON content
        if not request.is_json:
            return generate_response(
                message="Content-Type must be application/json",
                status_code=400
            )
        
        data = request.get_json()
        
        # Validate required fields
        errors = validate_book_data(data)
        if errors:
            return generate_response(
                message="Validation failed",
                status_code=400,
                error=errors
            )
        
        # Check if book with same ISBN already exists
        if data.get('isbn'):
            existing_book = next((book for book in books if book['isbn'] == data['isbn']), None)
            if existing_book:
                return generate_response(
                    message="Book with this ISBN already exists",
                    status_code=409
                )
        
        # Create new book
        new_book = {
            'id': str(uuid.uuid4()),
            'title': data['title'],
            'author': data['author'],
            'year': data['year'],
            'genre': data.get('genre', 'Unknown'),
            'isbn': data.get('isbn', ''),
            'rating': data.get('rating', 0.0),
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        books.append(new_book)
        
        return generate_response(
            data=new_book,
            message="Book created successfully",
            status_code=201
        )
        
    except Exception as e:
        return generate_response(
            message="Internal server error",
            status_code=500,
            error=str(e)
        )

@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book"""
    try:
        book = find_book(book_id)
        if not book:
            return generate_response(
                message="Book not found",
                status_code=404
            )
        
        if not request.is_json:
            return generate_response(
                message="Content-Type must be application/json",
                status_code=400
            )
        
        data = request.get_json()
        
        # Validate data
        errors = validate_book_data(data)
        if errors:
            return generate_response(
                message="Validation failed",
                status_code=400,
                error=errors
            )
        
        # Check ISBN uniqueness (if being updated)
        if data.get('isbn') and data['isbn'] != book['isbn']:
            existing_book = next((b for b in books if b['isbn'] == data['isbn'] and b['id'] != book_id), None)
            if existing_book:
                return generate_response(
                    message="Book with this ISBN already exists",
                    status_code=409
                )
        
        # Update book
        book.update({
            'title': data['title'],
            'author': data['author'],
            'year': data['year'],
            'genre': data.get('genre', book['genre']),
            'isbn': data.get('isbn', book['isbn']),
            'rating': data.get('rating', book['rating']),
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        })
        
        return generate_response(
            data=book,
            message="Book updated successfully"
        )
        
    except Exception as e:
        return generate_response(
            message="Internal server error",
            status_code=500,
            error=str(e)
        )

@app.route('/api/books/<book_id>', methods=['PATCH'])
def partial_update_book(book_id):
    """Partially update a book"""
    try:
        book = find_book(book_id)
        if not book:
            return generate_response(
                message="Book not found",
                status_code=404
            )
        
        if not request.is_json:
            return generate_response(
                message="Content-Type must be application/json",
                status_code=400
            )
        
        data = request.get_json()
        
        # Update only provided fields
        for field, value in data.items():
            if field in ['title', 'author', 'genre', 'isbn']:
                book[field] = value
            elif field == 'year':
                if not isinstance(value, int) or value < 1800 or value > 2024:
                    return generate_response(
                        message="Invalid year value",
                        status_code=400
                    )
                book[field] = value
            elif field == 'rating':
                if not isinstance(value, (int, float)) or value < 0 or value > 5:
                    return generate_response(
                        message="Rating must be between 0 and 5",
                        status_code=400
                    )
                book[field] = float(value)
        
        book['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        
        return generate_response(
            data=book,
            message="Book partially updated successfully"
        )
        
    except Exception as e:
        return generate_response(
            message="Internal server error",
            status_code=500,
            error=str(e)
        )

@app.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book"""
    book = find_book(book_id)
    
    if not book:
        return generate_response(
            message="Book not found",
            status_code=404
        )
    
    books.remove(book)
    
    return generate_response(
        message="Book deleted successfully",
        status_code=204
    )

# Additional API endpoints

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """Search books by query"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return generate_response(
            message="Search query parameter 'q' is required",
            status_code=400
        )
    
    # Search in title, author, and genre
    search_results = [
        book for book in books
        if (query in book['title'].lower() or
            query in book['author'].lower() or
            query in book['genre'].lower())
    ]
    
    return generate_response(
        data={'books': search_results, 'query': query},
        message=f"Found {len(search_results)} books matching '{query}'"
    )

@app.route('/api/books/stats', methods=['GET'])
def get_book_stats():
    """Get book statistics"""
    if not books:
        return generate_response(
            data={'total_books': 0},
            message="No books available"
        )
    
    # Calculate statistics
    total_books = len(books)
    genres = {}
    years = {}
    total_rating = 0
    
    for book in books:
        # Genre count
        genre = book['genre']
        genres[genre] = genres.get(genre, 0) + 1
        
        # Year count
        year = book['year']
        years[year] = years.get(year, 0) + 1
        
        # Rating sum
        total_rating += book['rating']
    
    avg_rating = total_rating / total_books if total_books > 0 else 0
    
    stats = {
        'total_books': total_books,
        'average_rating': round(avg_rating, 2),
        'genres': genres,
        'years': years,
        'oldest_book': min(books, key=lambda x: x['year'])['year'],
        'newest_book': max(books, key=lambda x: x['year'])['year']
    }
    
    return generate_response(
        data=stats,
        message="Book statistics retrieved successfully"
    )

@app.route('/api/books/bulk', methods=['POST'])
def bulk_create_books():
    """Create multiple books at once"""
    try:
        if not request.is_json:
            return generate_response(
                message="Content-Type must be application/json",
                status_code=400
            )
        
        data = request.get_json()
        books_data = data.get('books', [])
        
        if not isinstance(books_data, list):
            return generate_response(
                message="'books' must be an array",
                status_code=400
            )
        
        created_books = []
        errors = []
        
        for i, book_data in enumerate(books_data):
            try:
                # Validate book data
                book_errors = validate_book_data(book_data)
                if book_errors:
                    errors.append(f"Book {i+1}: {', '.join(book_errors)}")
                    continue
                
                # Check ISBN uniqueness
                if book_data.get('isbn'):
                    existing_book = next((book for book in books if book['isbn'] == book_data['isbn']), None)
                    if existing_book:
                        errors.append(f"Book {i+1}: ISBN already exists")
                        continue
                
                # Create book
                new_book = {
                    'id': str(uuid.uuid4()),
                    'title': book_data['title'],
                    'author': book_data['author'],
                    'year': book_data['year'],
                    'genre': book_data.get('genre', 'Unknown'),
                    'isbn': book_data.get('isbn', ''),
                    'rating': book_data.get('rating', 0.0),
                    'created_at': datetime.utcnow().isoformat() + 'Z',
                    'updated_at': datetime.utcnow().isoformat() + 'Z'
                }
                
                books.append(new_book)
                created_books.append(new_book)
                
            except Exception as e:
                errors.append(f"Book {i+1}: {str(e)}")
        
        return generate_response(
            data={
                'created_books': created_books,
                'total_created': len(created_books),
                'errors': errors
            },
            message=f"Bulk operation completed. {len(created_books)} books created, {len(errors)} errors.",
            status_code=201 if created_books else 400
        )
        
    except Exception as e:
        return generate_response(
            message="Internal server error",
            status_code=500,
            error=str(e)
        )

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return generate_response(
        message="Endpoint not found",
        status_code=404
    )

@app.errorhandler(405)
def method_not_allowed(error):
    return generate_response(
        message="Method not allowed",
        status_code=405
    )

@app.errorhandler(500)
def internal_error(error):
    return generate_response(
        message="Internal server error",
        status_code=500
    )

if __name__ == '__main__':
    print("Flask REST API Server")
    print("Available endpoints:")
    print("  GET  /api/books - Get all books")
    print("  GET  /api/books/<id> - Get specific book")
    print("  POST /api/books - Create new book")
    print("  PUT  /api/books/<id> - Update book")
    print("  PATCH /api/books/<id> - Partial update")
    print("  DELETE /api/books/<id> - Delete book")
    print("  GET  /api/books/search?q=<query> - Search books")
    print("  GET  /api/books/stats - Get statistics")
    print("  POST /api/books/bulk - Bulk create books")
    print("\nServer running at: http://localhost:5000")
    
    app.run(debug=True, port=5000)