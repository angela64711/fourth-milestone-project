def artist_status(request):
    user = request.user

    is_artist = user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Artists").exists()
    )

    return {"is_artist": is_artist}
