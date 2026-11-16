#!/usr/bin/env python3
"""天赋雷达本地服务：同源托管页面 + 反代 Magpie 网关 + 默认关闭的匿名数据池。"""
import http.server, urllib.request, json, sys, os
from datetime import datetime, timedelta, timezone

PORT = 8018
GATEWAY = 'http://127.0.0.1:3425'
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'contributions.jsonl')
RESEARCH_KEY = os.environ.get('TALENT_RADAR_RESEARCH_KEY', '')
WINDOW_DAYS = 30
REQUIRED = {'schema_version', 'contributor_hash', 'created_at', 'answers', 'scores', 'meta', 'consent'}


def validate_contribution(payload):
    """返回 True 或 False；只接受完整 schema + 显式同意的样本。"""
    if not isinstance(payload, dict) or not REQUIRED.issubset(payload):
        return False
    c = payload.get('consent', {})
    if not (isinstance(c, dict) and c.get('upload') is True and c.get('version') == '1.0'):
        return False
    m = payload.get('meta', {})
    if not isinstance(m, dict) or m.get('demo') is True:
        return False
    if payload.get('schema_version') != 1:
        return False
    if not isinstance(payload.get('contributor_hash'), str) or len(payload['contributor_hash']) < 8:
        return False
    try:
        datetime.fromisoformat(payload['created_at'].replace('Z', '+00:00'))
    except (ValueError, AttributeError, TypeError):
        return False
    return True


def is_effective(row, now=None):
    """有效样本：同意、非 demo、非直线作答、非中断、在 30 天窗口内。"""
    now = now or datetime.now(timezone.utc)
    try:
        ts = datetime.fromisoformat(row['created_at'].replace('Z', '+00:00'))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
    except (ValueError, KeyError, TypeError):
        return False
    if ts < now - timedelta(days=WINDOW_DAYS):
        return False
    m = row.get('meta', {})
    if m.get('demo') or m.get('straight_lined') or m.get('interrupted'):
        return False
    return validate_contribution(row)


def summary(path=None, window_days=WINDOW_DAYS):
    """按 contributor_hash 去重（保留最新），统计窗口内有效样本。"""
    path = path or DATA_FILE
    rows = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    by_hash = {}
    for r in rows:
        h = r.get('contributor_hash')
        if h:
            by_hash[h] = r  # 后面的（更新的）覆盖前面的
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=window_days)
    valid = []
    for r in by_hash.values():
        try:
            ts = datetime.fromisoformat(r['created_at'].replace('Z', '+00:00'))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except (ValueError, KeyError, TypeError):
            continue
        if ts >= cutoff and is_effective(r, now):
            valid.append(r)
    n = len(valid)
    if n >= 500:
        verdict = 'ready'
    elif n < 200:
        verdict = 'cut'
    else:
        verdict = 'collecting'
    return {
        'window_days': window_days, 'cutoff_at': cutoff.isoformat(), 'boundary_inclusive': True,
        'valid_n': n, 'total_n': len(rows),
        'invalid_n': len(rows) - n, 'ready': n >= 500, 'verdict': verdict,
    }


def _json_response(handler, payload, status=200):
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/api/contributions/summary':
            if not RESEARCH_KEY or self.headers.get('X-Research-Key') != RESEARCH_KEY:
                _json_response(self, {'error': 'research key required or not configured'}, 503)
                return
            _json_response(self, summary())
            return
        super().do_GET()

    def do_POST(self):
        path = self.path.split('?')[0]
        if path == '/api/contribute':
            if not RESEARCH_KEY:
                _json_response(self, {'error': 'data pool disabled: TALENT_RADAR_RESEARCH_KEY not configured'}, 503)
                return
            length = int(self.headers.get('Content-Length', 0))
            try:
                payload = json.loads(self.rfile.read(length))
            except json.JSONDecodeError:
                _json_response(self, {'error': 'invalid json'}, 400)
                return
            if not validate_contribution(payload):
                _json_response(self, {'error': 'invalid contribution'}, 400)
                return
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(DATA_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(payload, ensure_ascii=False) + '\n')
            _json_response(self, {'ok': True})
            return
        if not path.startswith('/v1/'):
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        req = urllib.request.Request(
            GATEWAY + self.path, data=body,
            headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data, status = r.read(), r.status
        except Exception as e:
            data, status = json.dumps({'error': {'message': str(e)}}).encode(), 502
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f'天赋雷达服务已启动: http://127.0.0.1:{port}  (Ctrl+C 停止)')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
