from enum import Enum


class Environment(Enum):
    QA = "qa"
    PROD = "prod"

    @classmethod
    def set_current_env(cls, env):
        if env not in Environment:
            raise TypeError("Unknown environment: %s" % env)

        cls._current_env = env

    @classmethod
    def get_current_env(cls):
        return cls._current_env

    @classmethod
    def get_environment_config(cls):
        if not cls._current_env:
            raise ValueError("Environment not set.")

        return QATestConfig if cls._current_env == Environment.QA else ProdTestConfig

# Current execution environment.
Environment._current_env = 'test'


class TestConfig(object):
    _config = {
        # Create Deployment AWS
        "deploymentNameAWS": "test_aws",
        "provider_region1": "US West (Oregon)",
        "provider_region2": "US West (N. California)",
        "provider_region3": "US East (N. Virginia)",
        "provider_region4": "EU (Ireland)",
        "provider_region5": "EU (Frankfurt)",
        "provider_region6": "Asia Pacific (Singapore)",
        "provider_region7": "Asia Pacific (Mumbai)",
        "provider_region8": "Asia Pacific (Sydney)",
        "provider_region9": "US East (Ohio)",
        "provider_region10": "Canada (Central)",
        "provider_region11": "EU (London)",
        "provider_region12": "Asia Pacific (Tokyo)",
        "provider_region13": "Asia Pacific (Seoul)",
        "provider_region14": "13",
        "solr_version": "6.6.2 - Recommended",

        # Create Deployment Azure
        "deploymentNameAzure": "test_azure",
        "provider_region_azure": "East US",

        # Create Threshold Alert
        "metric_name": "System Load Average",
        "operator": ">",
        "metric_value": "0.2",
        "metric_prefix": "number",
        "alert_name": "System Overload",
        "delay": "1",
        "max_alerts": "3",
        "repeat_every": "2",
        "notification_email": "automation@searchstax.com",

        # Sign Up Details
        "first_name": "Jon",
        "last_name": "Snow",
        "account_name": "jon_snow",
        "email1": "jon_snow@mailinator.com",
        "password1": "qwerty123",

        # Update Profile
        "phone_number": "+15005550006"
    }

    @classmethod
    def get_value(cls, config):
        if config not in cls._config:
            raise ValueError("Unknown config: %s." % config)

        return cls._get_value(config)

    @classmethod
    def _get_value(cls, config):
        raise NotImplementedError()


class QATestConfig(TestConfig):
    _config = TestConfig._config.copy()
    _config.update({
        "base_url": "https://app.searchstax.co",
        "email": "test@searchstax.co",
        "password": "test123456",
        "tenant": "AutomationTests",

        # Deployment plans
        "aws_plan_count": 158,
        "azure_plan_count": 6,
        "total_plan_count": 164
    })

    @classmethod
    def _get_value(cls, config):
        return cls._config[config]


class ProdTestConfig(TestConfig):
    _config = TestConfig._config.copy()
    _config.update({
        "base_url": "https://app.searchstax.com",
        "email": "automation@searchstax.com",
        "password": "test123456",
        "tenant": "test430",

        # Deployment plans
        "aws_plan_count": 148,
        "azure_plan_count": 6,
        "total_plan_count": 154
    })

    @classmethod
    def _get_value(cls, config):
        return cls._config[config]
