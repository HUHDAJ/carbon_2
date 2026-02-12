import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__, static_folder="src/web")
ROOT_DIR = Path(__file__).resolve().parent
DB_FILE = ROOT_DIR / "database" / "cbam_database.db"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败：{str(e)}")
        raise

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        raise ValueError(f"日期格式错误，需为YYYY-MM-DD：{date_str}")

# ---------- 接口1：CBAM预测数据 ----------
@app.route("/api/cbam/forecast", methods=["GET"])
def api_get_cbam_forecast():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM cbam_forecast", conn)
        conn.close()
        return jsonify({"code": 200, "data": df.to_dict(orient="records"), "msg": "CBAM预测数据读取成功"})
    except Exception as e:
        return jsonify({"code": 500, "data": None, "msg": f"读取失败：{str(e)}"}), 500

# ---------- 接口2：CEP碳因子预测 ----------
@app.route("/api/cep/carbon-factor", methods=["GET"])
def api_get_cep_carbon_factor():
    try:
        conn = get_db_connection()
        # ✅ 表名已统一为 cep_carbon_factor
        df = pd.read_sql("SELECT * FROM cep_carbon_factor", conn)
        conn.close()
        return jsonify({"code": 200, "data": df.to_dict(orient="records"), "msg": "CEP碳因子数据读取成功"})
    except Exception as e:
        return jsonify({"code": 500, "data": None, "msg": f"读取失败：{str(e)}"}), 500

# ---------- 接口3：每日碳因子全量 ----------
@app.route("/api/carbon-factor/daily-all", methods=["GET"])
def api_get_daily_carbon_factors_all():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM daily_carbon_factors_all", conn)
        conn.close()
        return jsonify({"code": 200, "data": df.to_dict(orient="records"), "msg": "每日碳因子全量数据读取成功"})
    except Exception as e:
        return jsonify({"code": 500, "data": None, "msg": f"读取失败：{str(e)}"}), 500

# ---------- 接口4：碳因子历史数据（按日期范围）----------
@app.route("/api/carbon-factor/history", methods=["GET"])
def api_get_carbon_factor_history():
    try:
        base_date_str = request.args.get("base_date")
        days_str = request.args.get("days")
        if not base_date_str or not days_str:
            return jsonify({"code": 400, "data": None, "msg": "参数缺失：需提供base_date和days"}), 400
        
        base_date = parse_date(base_date_str)
        days = int(days_str)
        start_date = base_date - timedelta(days=days)
        start_date_str = start_date.strftime("%Y-%m-%d")
        base_date_str = base_date.strftime("%Y-%m-%d")

        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM daily_carbon_factors_all", conn)
        conn.close()

        date_columns = [col for col in df.columns if col.lower() in ["date", "日期", "时间", "dt"]]
        if not date_columns:
            return jsonify({"code": 400, "data": None, "msg": "数据表中未找到日期列"}), 400
        date_col = date_columns[0]

        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        mask = (df[date_col] >= start_date_str) & (df[date_col] <= base_date_str)
        filtered_df = df[mask]

        return jsonify({
            "code": 200,
            "data": filtered_df.to_dict(orient="records"),
            "msg": f"获取{start_date_str}至{base_date_str}数据，共{len(filtered_df)}条"
        })
    except Exception as e:
        return jsonify({"code": 500, "data": None, "msg": f"读取历史数据失败：{str(e)}"}), 500

# ---------- 接口5：CBAM历史数据 ----------
@app.route("/api/cbam/history", methods=["GET"])
def api_get_cbam_history():
    try:
        base_date_str = request.args.get("base_date")
        days_str = request.args.get("days")
        if not base_date_str or not days_str:
            return jsonify({"code": 400, "data": None, "msg": "参数缺失：需提供base_date和days"}), 400

        base_date = parse_date(base_date_str)
        days = int(days_str)
        start_date = base_date - timedelta(days=days)
        start_date_str = start_date.strftime("%Y-%m-%d")
        base_date_str = base_date.strftime("%Y-%m-%d")

        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM cbam_forecast", conn)
        conn.close()

        date_columns = [col for col in df.columns if col.lower() in ["date", "日期", "时间", "dt"]]
        if not date_columns:
            return jsonify({"code": 400, "data": None, "msg": "CBAM表中未找到日期列"}), 400
        date_col = date_columns[0]

        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        mask = (df[date_col] >= start_date_str) & (df[date_col] <= base_date_str)
        filtered_df = df[mask]

        # 自动补充至7条
        if len(filtered_df) < 7:
            latest_df = df.sort_values(by=date_col, ascending=False).head(7)
            result_data = latest_df.to_dict(orient="records")
            msg = f"⚠️ 仅返回{len(filtered_df)}条，已自动补充至最新7条"
        else:
            result_data = filtered_df.to_dict(orient="records")
            msg = f"✅ 获取{start_date_str}至{base_date_str}数据，共{len(filtered_df)}条"

        return jsonify({"code": 200, "data": result_data, "msg": msg})
    except Exception as e:
        return jsonify({"code": 500, "data": None, "msg": f"读取CBAM历史数据失败：{str(e)}"}), 500

# ---------- 前端静态文件路由 ----------
@app.route("/")
def index():
    return app.send_static_file("agent/index.html")

@app.route("/<path:path>")
def serve_static(path):
    return app.send_static_file(path)

# ---------- 启动 ----------
if __name__ == "__main__":
    if not DB_FILE.exists():
        print("⚠️ 警告：数据库文件不存在，请先运行 __init__.py 初始化！")
    print("🚀 后端服务启动中...")
    print(f"🌐 访问地址：http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)