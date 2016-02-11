PROJECT_FOLDER="/var/www/PyTaskHelper"

python3 "$PROJECT_FOLDER/parser/courseparser.py"
python3 "$PROJECT_FOLDER/parser/statistics_maker.py"
python3 "$PROJECT_FOLDER/parser/category_db.py"
cd "$PROJECT_FOLDER/automatization"
./date.sh
cd "$PROJECT_FOLDER/site"
gulp
cd "$PROJECT_FOLDER/site/dist"
cp -rf * /var/www/pytask.info
cd /var/www/
chmod -R 755 pytask.info
chown -R avefablo:sudo pytask.info