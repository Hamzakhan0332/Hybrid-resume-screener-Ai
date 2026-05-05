@echo off
echo Setting up Resume Screener AI...
pip install -r requirements.txt
python -m spacy download en_core_web_md
echo Setup complete!
echo To run the CLI: python app.py --resume path/to/cv.pdf --jd path/to/jd.txt
echo To run the Web App: streamlit run streamlit_app.py
pause
