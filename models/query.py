import psycopg2
import psycopg2.extras
import os
from psycopg2.extras import execute_batch


def getUri():
  if 'ENV' in os.environ and os.environ['ENV'] == 'offline':
    return None
  if 'ENV' in os.environ and os.environ['ENV'] == 'prod':
    return os.environ['DATABASE_URL']
  elif os.environ['ENV'] in ['dev', 'staging']:
    return os.environ['FOLLOWER_DATABASE_URL']
  return os.environ['TEST_DATABASE_URL']

def filterByKey(l, key):
  output_list = []
  rollup_dict = {}

  for item in l:
    if item[key] is None:
      output_list.append(item)
      continue

    rollup_dict[item[key]] = rollup_dict.get(item[key], []) + [item]

  for dict_key in rollup_dict:
    output_list.append(rollup_dict[dict_key][0])

  return output_list

def executeBatch(query, values, ret=True):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor() as cur:
      execute_batch(cur, query, values)
      conn.commit()

      if not ret:
        return 'True'
      return cur.fetchall()

def dictFetchall(query, values=tuple(), decrypt=False, printResults=False):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
      cur.execute(query, values)
      ret = cur.fetchall()

      if not ret:
        if printResults:
          print(ret)
        return ret

      ret = [dict(x) for x in ret]

      if printResults:
        print(ret)
      return ret

def fetchall(query, values=tuple([]), log=False, decrypt=False, printResults=False):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor() as cur:
      if log:
        print(cur.mogrify(query, values))
      cur.execute(query, values)
      res = cur.fetchall()

      if decrypt:
        res = models.encryptionHelpers.decryptCollection(res)

      if printResults:
        print(res)

      return res


def dictFetchone(query, values=tuple([]), decrypt=False):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
      cur.execute(query, values)
      ret = cur.fetchone()

      if not ret:
        return ret

      ret = dict(ret)

      if decrypt:
        ret = models.encryptionHelpers.decryptRow(ret)

      return ret


def fetchone(query, values=tuple([]), log=False, decrypt=False):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor() as cur:
      if log:
        print(cur.mogrify(query, values))
      cur.execute(query, values)
      res = cur.fetchone()

      if decrypt:
        res = models.encryptionHelpers.decryptRow(res)

      if res and len(res) == 1:
        return res[0]
      return res

def insert(query, values, commit=True, ret=True):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor() as cur:
      cur.execute(query, values)
      if commit:
        conn.commit()
      if ret:
        return cur.fetchone()
      return

def execute(query, values, ret=True):
  uri = getUri()
  if uri is None:
    return []

  with psycopg2.connect(uri) as conn:
    with conn.cursor() as cur:
      cur.execute(query, values)
      conn.commit()
      if not ret:
        return 'True'
      res = cur.fetchone()
      if res and len(res) == 1:
        return res[0]
      return res
