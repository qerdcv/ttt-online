# Server Actions Status

[![Lint](https://github.com/qerdcv/ttt-online/actions/workflows/linter.yml/badge.svg)](https://github.com/qerdcv/ttt-online/actions/workflows/linter.yml)
[![Tests](https://github.com/qerdcv/ttt-online/actions/workflows/tests.yml/badge.svg)](https://github.com/qerdcv/ttt-online/actions/workflows/tests.yml)
[![ESLint](https://github.com/qerdcv/ttt-online/actions/workflows/eslint.yml/badge.svg)](https://github.com/qerdcv/ttt-online/actions/workflows/eslint.yml)
[![Deploy Backend](https://github.com/qerdcv/ttt-online/actions/workflows/deploy-backend.yml/badge.svg)](https://github.com/qerdcv/ttt-online/actions/workflows/deploy-backend.yml)
[![Deploy Frontend](https://github.com/qerdcv/ttt-online/actions/workflows/deploy-front.yml/badge.svg)](https://github.com/qerdcv/ttt-online/actions/workflows/deploy-front.yml)

# ttt-online

TicTacToe Online

# Server part of TTT-online

## Generate salt for hashing password

```python
import random
from string import printable

salt = list(printable.strip())
random.shuffle(salt)
result = ''.join(salt)
```

## TESTS

---

### Integration</h3>

- **Requirements**

  - Docker
  - docker-compose
  - Make

- **Usage**
  - make test-integration
