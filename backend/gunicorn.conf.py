"""Linux / Docker 生产配置。限流在内存中，先保持单进程。"""
import os

bind = f'0.0.0.0:{os.getenv("PORT", "10000")}'
workers = 1
threads = 4
timeout = 120
accesslog = '-'
errorlog = '-'
