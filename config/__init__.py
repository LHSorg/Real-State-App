class Config:
    """Base config."""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'INFO'
    #   
    GCP_PROJECT = 'real-310017'
    BIGQUERY_TABLE = 'table_real.realstates'

class DevConfig(Config):
    """Dev config."""
    LOG_LEVEL = 'DEBUG'

class TestConfig(Config):
    """Test config."""
    TESTING = True