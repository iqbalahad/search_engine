import tarfile

def stream_collection(tar_path, prefix='collection'):
    """
    Streaming-Import aus tar.gz ohne vollständiges Entpacken.
    Yields jeweils eine Zeile (String) pro Dokument.
    """
    with tarfile.open(tar_path, 'r|gz') as tar:
        for member in tar:
            if member.isfile() and member.name.startswith(prefix):
                f = tar.extractfile(member)
                for line in f:
                    yield line.decode('utf-8').rstrip('\n')