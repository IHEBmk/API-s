from supabase import create_client

class SupabaseClientSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create and store the Supabase client
            cls._instance = create_client(
                'https://leerygjkvxnmesgnaiit.supabase.co',  
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxlZXJ5Z2prdnhubWVzZ25haWl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM3NTUxNTcsImV4cCI6MjA0OTMzMTE1N30.unNkWDmWvefen7QebVH00aqcgGcX6Y-058KyIBic8zA'  
            )
        return cls._instance

    def __init__(self, url=None, key=None):
      
        if url and key:
            self.client = create_client(url, key)
        else:
            self.client = self._instance
