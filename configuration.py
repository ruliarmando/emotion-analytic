

class BaseConfig(object):
    """Base config class"""
    SECRET_KEY = 'ar0ckc0ekcnodie$s0c1s03n3'
    DEBUG = True
    TESTING = False
    
    CONSUMER_KEY = 'nvumVrgGibGYoKdu5znHXNTnP'
    CONSUMER_SECRET = '6elLz7cT039aitC7vdKamEsotpSfWf1CpsJKvneuNl35SfW0g2'
    ACCESS_TOKEN = '220186959-xkjlij0hTKL3Ho9ipr3uqezXGtrbpkkLRsosjmWo'
    ACCESS_TOKEN_SECRET = '4cU8DFiyh84VAZwUuMZgc8zDUwpi6qgLlgonFHr5cpj1T'


class ProductionConfig(BaseConfig):
    """Production Specific config"""
    DEBUG = False
    SECRET_KEY = 'ar0ckc0ekcnodie$s0c1s03n3d0j2ld0end;spp3kdl'


class StagingConfig(BaseConfig):
    """Staging Specific config"""
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True