# Called once per day (6:30am by default).
# Invokes weather forecast and sudoku-gfx scripts.
def daily():
  GPIO.output(ledPin, GPIO.HIGH)
  subprocess.call(["python", "forecast.py"])
  subprocess.call(["python", "sudoku-gfx.py"])
  subprocess.call(["python", "lunch.py"])
  GPIO.output(ledPin, GPIO.LOW)