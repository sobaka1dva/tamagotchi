def get_health(health):
    return '❤️' * health


def get_image_path(health):
    if health <= 6:
        return 'red.jpg'
    elif health <= 13:
        return 'yellow.jpeg'
    else:
        return 'green.jpeg'

