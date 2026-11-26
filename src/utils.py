def reconstruct_path(prev, source, target):
    """Walk predecessor map backwards; return [] if target unreachable."""
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []
