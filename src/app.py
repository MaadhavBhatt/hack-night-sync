import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .config import check_environment_variables
from .handlers import handle_hack_night_command


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

app.command("/hack-night")(handle_hack_night_command)
app.command("/hacknight")(handle_hack_night_command)


if __name__ == "__main__":
    check_environment_variables()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
