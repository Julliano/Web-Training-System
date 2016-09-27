import sys

from consultoria import create_app

mode = 'production'
if (len(sys.argv) > 1) and (sys.argv[1] != 'db'):
    mode = sys.argv[1] 
    
app = create_app(mode=mode)


if __name__ == "__main__":
    app.run(**app.config.get_namespace('RUN_'))
    
