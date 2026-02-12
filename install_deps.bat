@echo off
echo 正在安装Python依赖...
pip install fastapi uvicorn[standard] pydantic pandas numpy
echo 依赖安装完成！
echo.
echo 启动服务器:
echo python run_backend.py
pause