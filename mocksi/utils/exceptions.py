

class ConfigException(Exception):
    pass


class DockerException(Exception):
    pass


class NotFoundFileException(ConfigException):
    pass


class ConfigFileEmptyException(ConfigException):
    pass


class NotFoundImageException(DockerException):
    pass


class NotFoundContainerException(DockerException):
    pass
