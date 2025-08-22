from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """Create and return a Supabase client instance."""
    supabase: Client = create_client(
        settings.SUPABASE_URL, 
        settings.SUPABASE_SERVICE_KEY
    )
    return supabase

# Global client instance
supabase_client = get_supabase_client()
