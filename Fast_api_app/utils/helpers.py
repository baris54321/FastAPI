def has_exception(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return {
                "error": str(e),
                "message": "An error occurred while processing your request."
            }
    return wrapper
