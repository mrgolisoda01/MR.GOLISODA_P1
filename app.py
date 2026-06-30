"""MR.GOLISODA — Flask backend + Supabase persistence."""
import os
from flask import Flask, render_template, request, jsonify

from supabase import create_client


app = Flask(__name__)

SUPABASE_URL ="https://zysvftmuacguuzzgceyt.supabase.co"
SUPABASE_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5c3ZmdG11YWNndXV6emdjZXl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MDU4MTAsImV4cCI6MjA5ODM4MTgxMH0.zMYR9QQLBvC_S51AmuCZQoYuo_hLrooPBFzx2ixgE_Q"
sb = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
TABLE = "app_state"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state/<key>", methods=["GET"])
def get_state(key):
    if not sb:
        return jsonify({}), 200
    res = sb.table(TABLE).select("data").eq("key", key).execute()
    if res.data:
        return jsonify(res.data[0]["data"]), 200
    return jsonify({}), 200


@app.route("/api/state/<key>", methods=["PUT", "POST"])
def put_state(key):
    if not sb:
        return jsonify({"ok": False, "msg": "Supabase not configured"}), 200
    payload = request.get_json(force=True, silent=True) or {}
    sb.table(TABLE).upsert({"key": key, "data": payload}).execute()
    return jsonify({"ok": True}), 200


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "supabase": bool(sb)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
