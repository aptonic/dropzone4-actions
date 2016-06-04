is_determinate = True
last_output_percent = 0

def set_determinate_progress(determinate):
    global is_determinate
    if is_determinate and not determinate:
        dz.determinate(False)
        is_determinate = False
    elif not is_determinate and determinate:
        dz.determinate(True)
        is_determinate = True   

def set_progress_percent(percent):
    global last_output_percent
    if percent > last_output_percent:
        dz.percent(percent)
        last_output_percent = percent
        
def reset_progress():
    global last_output_percent
    last_output_percent = 0