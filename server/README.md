# **_TTT-online server information_** 

## Useful command
***
### Generate secret key for encrypt
```python
from cryptography.fernet import Fernet
KEY = Fernet.generate_key()
print(KEY.decode('utf-8'))
``` 
