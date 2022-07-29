from sys import version

if version[0] == "3":
    from functools import partial

    from six import ensure_str

    str_handler = partial(bytes, encoding="utf-8")

    def call_ret_str(f, *args, **kwargs):
        res = f(*args, **kwargs)
        return ensure_str(res) if isinstance(res, bytes) else res

    def call_ret_str_cast_first_arg(f, *args, **kwargs):
        res = f(
            *(
                ((bytes(args[0], "utf-8"),) + (args[1:] if len(args) > 1 else tuple()))
                if args and isinstance(args[0], str)
                else args
            ),
            **kwargs
        )
        return ensure_str(res) if isinstance(res, bytes) else res

else:

    def identity(*args):
        return args[0] if len(args) == 1 else args

    def identity_func(f, *args, **kwargs):
        return f(*args, **kwargs)

    str_handler = identity
    call_ret_str = call_ret_str_cast_first_arg = identity_func


__all__ = ["str_handler", "call_ret_str", "call_ret_str_cast_first_arg"]
