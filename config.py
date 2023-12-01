# config.py

TOKEN = '5737847651:AAF1ZUqhMXfiWgi-tKhIodptISo9SwW6y_g'
api_key = 'sk-1NhZl248eEDdB0454BAbT3BLbkFJEB661cec99274eD58C61'
base_url = 'https://aigptx.top/v1'
model = 'gpt-4-1106-preview'  # 模型配置
voice = 'nova'  # Supported voices are alloy, echo, fable, onyx, nova, and shimmer.
role = "你是一个热心肠的学姐，善于解答学弟们各种奇怪的问题"  # role配置
REQUEST_KWARGS = {
    'con_pool_size': 8,  # 设置连接池大小
    'read_timeout': 15,  # 设置读取超时时间
    'connect_timeout': 15,  # 设置连接超时时间
    'proxy_url': 'http://127.0.0.1:7890',  # 代理配置
    # 可选，如果你的代理需要认证，还可以添加代理用户名和密码
    # 'urllib3_proxy_kwargs': {
    #     'username': 'PROXY_USER',
    #     'password': 'PROXY_PASS',
    # }
}
max_context_limit: 20  # 最大上下文长度
