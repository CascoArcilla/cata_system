import cloudinary.api

def revisar_uso_cloudinary():
    try:
        usage = cloudinary.api.usage()
        
        storage = usage.get('storage', {}) if isinstance(usage, dict) else getattr(usage, 'storage', {})
        used_bytes = storage.get('usage', 0) if isinstance(storage, dict) else 0
        limit_bytes = storage.get('limit', 0) if isinstance(storage, dict) else 0
        percentage = storage.get('used_percent', 0) if isinstance(storage, dict) else 0

        used_mb = round(used_bytes / (1024 * 1024), 2) if isinstance(used_bytes, (int, float)) else 0
        limit_mb = round(limit_bytes / (1024 * 1024), 2) if isinstance(limit_bytes, (int, float)) else 0

        return {
            'used_mb': used_mb,
            'limit_mb': limit_mb,
            'percentage': percentage,
            'error': False
        }
    except Exception as e:
        print(f"Excepción en Cloudinary API: {e}")
        return {
            'used_mb': 0,
            'limit_mb': 0,
            'percentage': 0,
            'error': True
        }
