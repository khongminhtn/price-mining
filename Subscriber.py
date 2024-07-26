import requests
from util import tprint

def sub(chart_id, table, period, session, control):
  # Subscribe to chart
  endpoint = f"https://{control}/lightstreamer/control.txt"
  payload = {
    "LS_session": session,
    "LS_op": "add",
    "LS_table": table,
    "LS_id": f'CHART:{chart_id}:{period}',
    "LS_schema": "BID OFR",
    "LS_mode": "DISTINCT"
  }
  res = requests.post(endpoint, data=payload)
  tprint(f'Chart Sub: {payload["LS_id"]} | {res.status_code}')


sub("CS.D.EURUSD.TODAY.IP", "1", "TICK", 'S2fe7e97bbb3fb831M888T2433342', "apd249f.marketdatasystems.com")
sub("CS.D.GBPUSD.TODAY.IP", "2", "TICK", 'S2fe7e97bbb3fb831M888T2433342', "apd249f.marketdatasystems.com")