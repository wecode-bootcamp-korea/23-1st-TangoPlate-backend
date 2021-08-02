DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tangoplate_db',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1', #데이터베이스의 IP주소, 이건 각자의 컴퓨터
        'PORT': '3306',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9fyga)5y0xk9whbhnihtrjgq)4pq5a^j(zc5ez&emr75ooyr_2'

APPEND_SLASH = False