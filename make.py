from flask import Flask, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Attendance App UI Mockup</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #ffffff;
      color: #333333;
    }

    /* Top Nav */
    .navbar {
      background: linear-gradient(to right, #004f4f, #006d6d);
      color: #ffffff;
      padding: 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .nav-center {
      text-align: center;
      flex: 1;
    }

    .subject-name {
      font-size: 1.2rem;
      margin: 0;
      font-weight: bold;
    }

    .subject-code {
      font-size: 0.9rem;
      margin: 0;
    }

    .nav-button {
      background: none;
      border: none;
      color: #ffffff;
      cursor: pointer;
      font-size: 0.9rem;
      margin: 0 0.5rem;
    }

    /* Main Section */
    .main {
      padding: 1rem;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }

    .controls {
      display: flex;
      align-items: center;
      margin-bottom: 1rem;
    }

    .stat-button {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background-color: #ff8c00; /* Orange color */
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-weight: bold;
      margin-right: 1rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      cursor: pointer;
    }

    .calendar-buttons {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .calendar-button {
      width: 50px;
      height: 30px;
      background-color: #006d6d;
      color: #ffffff;
      border-radius: 5px;
      border: none;
      cursor: pointer;
      font-size: 0.8rem;
      font-weight: bold;
      position: relative;
    }

    .calendar-button span {
      display: block;
      margin-top: 35px; /* date label below button */
      font-size: 0.8rem;
      color: #333333;
    }

    /* Heading & Add Student Button */
    .section-header {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
    }

    .section-title {
      font-size: 1.2rem;
      font-weight: bold;
      margin: 0;
    }

    .add-student-btn {
      background-color: #006d6d;
      color: #ffffff;
      border: none;
      border-radius: 5px;
      padding: 0.5rem 1rem;
      cursor: pointer;
      font-size: 0.9rem;
      display: none; /* default hidden, show when date is selected */
    }

    /* Leaderboard/Records List */
    .list-container {
      width: 100%;
      border: 1px solid #dddddd;
      border-radius: 5px;
      padding: 1rem;
      max-height: 300px;
      overflow-y: auto;
    }

    .list-item {
      display: flex;
      justify-content: space-between;
      padding: 0.5rem 0;
      border-bottom: 1px solid #eeeeee;
    }

    .list-item:last-child {
      border-bottom: none;
    }

    /* Bottom Slider/Button */
    .download-section {
      width: 100%;
      text-align: center;
      margin-top: 1rem;
   

    """
    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(debug=True)
