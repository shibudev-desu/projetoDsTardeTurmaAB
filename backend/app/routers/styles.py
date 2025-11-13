from fastapi import APIRouter
from app.models import Styles
from app.db.supabase_client import get_supabase


@router.get("/selectstyles")
def get_styles():
    supabase = get_supabase()
    response = supabase.table("styles").select("*").execute()
    return response.data  

@router.get("/styles/{styles_id}")
def get_styles_by_id(styles_id: int):
    supabase = get_supabase()
    response = supabase.table("styles").select("*").eq("id", styles_id).execute()
    if response.data:
        return response.data[0]
    return {"error": "style not found"}

@router.post("/styles")
def create_style(styles: Styles):
    supabase = get_supabase()
    new_style = {
       "name": styles.name,
        
    }
    response = supabase.table("styles").insert(new_style).execute()
    if response.data:
        return response.data[0]
    return {"error": "Failed to create style"} 