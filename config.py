
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    S3_BUCKET = "####"
    USE_BUCKET = True

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    USE_BUCKET = False

class TestingConfig(Config):
    TESTING = True