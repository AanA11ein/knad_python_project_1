def readable_size(size: int) -> str:
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    s = float(size)
    for unit in units:
        if s < 1024 or unit == units[-1]:
            if unit == 'B':
                return f'{int(s)} {unit}'
            return f'{s:.2f} {unit}'
        s /= 1024
    return f'{s:.2f} PB'