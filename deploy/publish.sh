SCRIPT_DIR=$(dirname $0)

cd $SCRIPT_DIR/..

# Clean old build
rm dist/*

python -m build
python -m twine upload dist/*
