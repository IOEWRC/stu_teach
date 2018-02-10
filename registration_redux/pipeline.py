


def get_avatar(backend, user, response, social_user, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        profile_image_url = response['image'].get('url')
        first_name = social_user['first_name']
        last_name = social_user['last_name']
        ext = url.split('.')[-1]
    if url:
        # user.profile.avatar = url
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user.profile.save()

