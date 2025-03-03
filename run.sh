# Open terminal with 2 tabs (front and back);
TERMINAL_ID=$(gnome-terminal --tab --title="frontend" --command="bash ./run-front.sh" \
                             --tab --title="backend" --command="bash ./run-back.sh" & sleep 1; wmctrl -l | grep "frontend" | awk '{print $1}')

# Focus on Terminal opened;
wmctrl -i -a "$TERMINAL_ID"
