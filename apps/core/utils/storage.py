# File storage configuration
FILE_UPLOAD_CONFIG = {
    'MAX_FILE_SIZE': 52428800,  # 50MB in bytes
    'ALLOWED_MIME_TYPES': {
        # Images
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/gif': ['.gif'],

        # Documents
        'application/pdf': ['.pdf'],
        'application/msword': ['.doc'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/vnd.ms-excel': ['.xls'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],

        # Archives
        'application/zip': ['.zip'],
        'application/x-rar-compressed': ['.rar'],

        # Others
        'text/plain': ['.txt'],
        'text/csv': ['.csv'],
    },

    # File categories and their paths
    'CATEGORIES': {
        'invoices': {
            'path': 'invoices',
            'allowed_types': ['.pdf', '.png', '.jpg'],
            'max_size': 10485760  # 10MB
        },
        'products': {
            'path': 'products',
            'allowed_types': ['.png', '.jpg'],
            'max_size': 5242880  # 5MB
        },
        'documents': {
            'path': 'documents',
            'allowed_types': ['.pdf', '.doc', '.docx'],
            'max_size': 52428800  # 50MB
        },
    },

    # Image specific settings
    'IMAGE_SIZES': {
        'thumbnail': (300, 300),
        'medium': (800, 800),
        'large': (1200, 1200)
    }
}
