import contextvars

user_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar('user_id', default=None)

