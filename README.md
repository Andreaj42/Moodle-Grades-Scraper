# Moodle Scraper 
1) Modify the config file **config/config.py** with your credentials (a template is available: **config/config.py.tpl**).
2) Modify the variable path to match your environment.
3) In the file **main.py**, run `MootseInit()` once to initialize the **url.txt** file.
```python 
if __name__ == "__main__":
    MootseInit()
    #MootseRunner().run_check()
```
5) Make sure not to have two different URLs for the same label 
6) In the file **main.py**, comment the line `MootseInit()` and uncomment `MootseRunner().run_check()`.
```python 
if __name__ == "__main__":
    #MootseInit()
    MootseRunner().run_check()
```
8) Use a task scheduler like systemd to run main.py

## Installation
```bash
pip install -e .
python main.py
```
