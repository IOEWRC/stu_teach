from social_core.backends.google import GoogleOAuth2


def update_user_social_data(strategy, *args, **kwargs):
    """
    Set the name and avatar for a user only if is new.
    """
    if not kwargs['is_new']:
        return
    backend = kwargs['backend']
    user = kwargs['user']

    if isinstance(backend, GoogleOAuth2):
        if kwargs['response'].get('image') and kwargs['response'].get('image').get('url'):
            url = kwargs['response'].get('image').get('url')
            url = url.split('?')[0] + '?sz=500'
            user.profile.socio_auth_avatar = url
    user.profile.save()
