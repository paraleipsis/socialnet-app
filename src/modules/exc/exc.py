from fastapi import FastAPI

from modules.exc.handlers import globals, posts


def init_exc_handlers(application: FastAPI) -> None:
    # globals
    application.add_exception_handler(Exception, globals.global_exception_handler)
    application.add_exception_handler(ConnectionRefusedError, globals.connection_refused_exception_handler)
    application.add_exception_handler(globals.AlreadyExistException, globals.already_exist_exception_handler)

    # posts
    application.add_exception_handler(posts.NoSuchPost, posts.post_not_exists_exception_handler)
    application.add_exception_handler(posts.UserVoteError, posts.user_vote_exception_handler)
