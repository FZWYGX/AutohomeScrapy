# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 97
INITIAL_SCORE = 99

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 45
# 获取周期
GETTER_CYCLE = 240

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'https://car.autohome.com.cn/pic/index.html'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10

# 这里url为你的讯代理api接口
XdailiUrl = ' '