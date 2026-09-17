# uso: ./env.sh script.py
export PYTHONIOENCODING=utf-8
exec uv run --no-project --python 3.12 --with nltk==3.8.1 --with scikit-learn==1.6.1 --with pandas==2.2.3 --with numpy==2.0.2 --with scipy==1.14.1 python "$@"
