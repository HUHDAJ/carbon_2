import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict

def init_carbon_database() -> None:
    ROOT_DIR = Path(__file__).resolve().parent
    DB_FILE = ROOT_DIR / "database" / "cbam_database.db"
    
    # 表名 → CSV文件路径（已修正表名）
    CSV_FILES: Dict[str, Path] = {
        "cbam_forecast": ROOT_DIR / "data" / "results" / "predict" / "CBAM" / "forecast.csv",
        "cep_carbon_factor": ROOT_DIR / "data" / "results" / "predict" / "CEP" / "carbon_forecast_20251228_20260923_20260212_144844.csv",
        "daily_carbon_factors_all": ROOT_DIR / "data" / "results" / "carbon_factors" / "daily_carbon_factors_all.csv"
    }

    # 自动创建database目录
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 检查CSV是否存在
    missing_files = [str(path) for table, path in CSV_FILES.items() if not path.exists()]
    if missing_files:
        raise FileNotFoundError(f"以下CSV文件不存在：{', '.join(missing_files)}")

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"✅ 连接数据库：{DB_FILE}")
        for table_name, csv_path in CSV_FILES.items():
            print(f"\n📄 处理文件：{csv_path}")
            df = pd.read_csv(
                csv_path,
                encoding="utf-8-sig",
                sep=",",
                na_filter=False,
                on_bad_lines='skip',
                low_memory=False
            )
            # 写入数据库（若表存在则覆盖）
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists="replace",
                index=False,
                chunksize=1000
            )
            print(f"   ✅ 导入 {table_name}，共 {len(df)} 行")
    except Exception as e:
        raise RuntimeError(f"数据库初始化失败：{str(e)}")
    finally:
        if conn:
            conn.close()
            print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    try:
        init_carbon_database()
        print("\n🎉 数据库初始化完成！")
    except Exception as e:
        print(f"\n❌ 初始化失败：{str(e)}")