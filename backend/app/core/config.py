import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

SUPABASE_STORAGE_BUCKET = os.getenv(
    "SUPABASE_STORAGE_BUCKET",
    "product-images",
)


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured"
    )


if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL is not configured"
    )


if not SUPABASE_SERVICE_KEY:
    raise RuntimeError(
        "SUPABASE_SERVICE_KEY is not configured"
    )