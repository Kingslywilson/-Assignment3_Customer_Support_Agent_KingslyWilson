import time
import functools
from typing import Callable, Any


def with_tool_retry(max_retries: int = 2):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            total_attempts = max_retries + 1

            for attempt in range(1, total_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, str) and result.startswith("TEMPORARY_ERROR:"):
                        raise RuntimeError(result.replace("TEMPORARY_ERROR:", "").strip())
                    return result
                except Exception as e:
                    last_error = e
                    if attempt <= max_retries:
                        print(
                            f"\n[RETRY WARN] Tool '{func.__name__}' encountered temporary error (Attempt {attempt}/{total_attempts}): {e}. "
                            f"Retrying ({attempt}/{max_retries})..."
                        )
                        time.sleep(0.3)
                    else:
                        print(
                            f"\n[RETRY EXHAUSTED] Tool '{func.__name__}' failed after {max_retries} retries. "
                            f"Returning graceful fallback message."
                        )
                        return (
                            "We are currently experiencing temporary technical issues with this service. "
                            "Please try again later."
                        )
        return wrapper
    return decorator
