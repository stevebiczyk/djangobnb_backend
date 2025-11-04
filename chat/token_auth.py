from django.contrib.auth.models import AnonymousUser
from django.channels.db import database_sync_to_async
from channels.middleware.base import BaseMiddleware

from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload['user_id']
        return User.objects.get(pk=user_id)
    except Exception as e:
        return AnonymousUser()
    
class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes a token from the query string
    and authenticates the user for WebSocket connections.
    """
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        query = dict((x.split('=') for x in scope['query_string'].decode().split('&')))
        token_key = query.get('token', None)
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)
    
        
    