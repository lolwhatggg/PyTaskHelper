PROJECT_FOLDER="/Volumes/Shared/Programming/AnyTaskAnalyzer"

python3 "$PROJECT_FOLDER/parser/courseparser.py"
python3 "$PROJECT_FOLDER/parser/statistics_maker.py"
cd "$PROJECT_FOLDER/site"
gulp