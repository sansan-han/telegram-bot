# config.py

TOKEN = '5737847651:AAF1ZUqhMXfiWgi-tKhIodptISo9SwW6y_g'
api_key = 'sk-1NhZl248eEDdB0454BAbT3BLbkFJEB661cec99274eD58C61'
base_url = 'https://aigptx.top/v1'
model = 'gpt-4-1106-preview'  # 模型配置
voice = 'nova'  # Supported voices are alloy, echo, fable, onyx, nova, and shimmer.
role = "you are a helpful assistant "  # role配置
REQUEST_KWARGS = {
    'con_pool_size': 8,  # 设置连接池大小
    'proxy_url': 'http://127.0.0.1:7890',  # 代理配置
    # 可选，如果你的代理需要认证，还可以添加代理用户名和密码
    # 'urllib3_proxy_kwargs': {
    #     'username': 'PROXY_USER',
    #     'password': 'PROXY_PASS',
    # }
}
max_context_limit: 20  # 最大上下文长度
