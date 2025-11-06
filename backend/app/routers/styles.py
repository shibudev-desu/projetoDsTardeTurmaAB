from fastapi import APIRouter
from app.models import Styles
from app.db.supabase_client import get_supabase


@router.get("/selectstyles")
def get_styles():
    supabase = get_supabase()
    response = supabase.table("styles").select("*").execute()
    return response.data  

