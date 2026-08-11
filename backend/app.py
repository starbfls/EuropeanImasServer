from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── 数据加载 ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / 'data'

def load_data(filename: str) -> list:
    """从 data/ 目录读取 JSON 文件并返回列表。"""
    path = DATA_DIR / filename
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── API 路由 ──────────────────────────────────────────────────────────────────

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    data = load_data('announcements.json')
    return jsonify({"success": True, "data": data})


@app.route('/api/announcements/<int:item_id>', methods=['GET'])
def get_announcement_detail(item_id):
    data = load_data('announcements.json')
    item = next((a for a in data if a["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "未找到"}), 404
    return jsonify({"success": True, "data": item})


@app.route('/api/event-records', methods=['GET'])
def get_event_records():
    data = load_data('event_records.json')
    return jsonify({"success": True, "data": data})


@app.route('/api/event-records/<int:item_id>', methods=['GET'])
def get_event_record_detail(item_id):
    data = load_data('event_records.json')
    item = next((r for r in data if r["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "未找到"}), 404
    return jsonify({"success": True, "data": item})


@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    data = load_data('gallery.json')
    return jsonify({"success": True, "data": data})


@app.route('/api/business-cards', methods=['GET'])
def get_business_cards():
    data = load_data('business_cards.json')
    approved = [c for c in data if c.get("approved")]
    return jsonify({"success": True, "data": approved})


@app.route('/api/business-cards', methods=['POST'])
def submit_business_card():
    # Mock: always returns success (real upload logic TBD)
    return jsonify({
        "success": True,
        "message": "名片已提交，正在审核中。审核通过后将显示在名片墙上。"
    }), 201


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "欧洲偶像大师制作人联盟服务器运行中"})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
