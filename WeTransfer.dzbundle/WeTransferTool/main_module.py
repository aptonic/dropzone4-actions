import argparse
from WeTransferTool import We
import json

def main_func():
    parser = argparse.ArgumentParser()
    wet = We()

    parser.add_argument('-dl', help="Wetransfer file URL", type=str)
    parser.add_argument('-ul', help="File/Folder path", type=str)
    parser.add_argument('-mw', help="Maximum number of workers (parallel downloads)", type=int, default=10)
    args = parser.parse_args()
    dl = args.dl
    ul = args.ul
    mw = args.mw
    if not dl and not ul:
        print("Need atleast one argument. Try wetransfertool -h")
    if ul:
        print(json.dumps(wet.upload(path=ul, max_workers=mw), indent=4))
    if dl:
        wet.download(dl)
    
# if __name__=="__main__":
#     main_func()