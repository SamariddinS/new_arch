from celery.backends.database.session import SessionManager as CelerySessionManager


class SessionManager(CelerySessionManager):
    """
    Override celery SessionManager
    """

    def __init__(self) -> None:
        super().__init__()

        # Disable automatic creation of celery internal task result table
        self.prepared = True
