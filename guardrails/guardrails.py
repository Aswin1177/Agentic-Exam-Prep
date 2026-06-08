from functools import wraps

def require_keys(*required_keys):

    def decorator(func):

        @wraps(func)
        def wrapper(state,*args,**kwargs):

            missing=[
                key for key in required_keys
                if key not in state
            ]

            if missing:
                raise ValueError(
                    f"{func.__name__}: Missing state keys {missing}"
                )

            return func(state,*args,**kwargs)

        return wrapper

    return decorator


def validate_output(*required_keys):

    def decorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):

            result=func(*args,**kwargs)

            if not isinstance(result,dict):
                raise TypeError(
                    f"{func.__name__} must return dict"
                )

            for key in required_keys:

                if key not in result:
                    raise ValueError(
                        f"{func.__name__}: Missing output key '{key}'"
                    )

            return result

        return wrapper

    return decorator


def retry(max_attempts=3):

    def decorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):

            last_exception=None

            for _ in range(max_attempts):

                try:
                    return func(*args,**kwargs)

                except Exception as e:
                    last_exception=e

            raise last_exception

        return wrapper

    return decorator