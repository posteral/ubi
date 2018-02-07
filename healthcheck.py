# This script executes heathcheck queries on a set of services
from env import Env

TEST_ENV = Env.NEXT2

print(TEST_ENV.pages_comparator_base_uri())