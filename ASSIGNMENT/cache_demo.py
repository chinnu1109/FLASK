from time import time
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

# Enable cache
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)

@app.route('/marks')
@cache.cached(timeout=30)   # cache for 30 seconds
def get_marks():
    print("FETCHING FROM DATABASE")
    return {
        "name": "Raju",
        "marks": 95
    }

if __name__ == '__main__':
    app.run(debug=True)


# Without cache
# Every request → data is fetched from database

# With cache

# First request → data fetched from database
# Data is stored in cache
# For 30 seconds → data comes from cache
# After 30 seconds → cache expires
# Next request → data fetched from database again
# Stored again in cache

# When to Use Cache
# ✅ Product lists
# ✅ Dashboard data
# ✅ Static configurations

# 🚫 When NOT to Use Cache

# ❌ Bank balance
# ❌ Live transactions
# ❌ OTPs



# from flask import Flask
# from flask_caching import Cache

# app.config['CACHE_TYPE'] = 'SimpleCache'
# cache = Cache(app)

# app.route('/marks'  )
# cache.Cached(timeout=30)

# def marks():
#     print("fetch from db")
#     return{
#         "name": "Raju",
#         "marks": 95
#     }

# if __name__ == '__main__':
#     app.run(debug=True)