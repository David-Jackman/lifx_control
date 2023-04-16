from flask import Flask, render_template, request, redirect, url_for
import lifx

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    lights = lifx.get_lights()
    if request.method == 'POST':
        selected_lights = request.form.getlist('lights')
        action = request.form['action']

        if action == 'toggle':
            for light_id in selected_lights:
                lifx.toggle_light(light_id)
        elif action == 'set_color':
            new_color = request.form['color']
            brightness = float(request.form['brightness'])
            duration = float(request.form['duration'])
            for light_id in selected_lights:
                lifx.set_color(light_id, new_color, brightness, duration)

        return redirect(url_for('index'))

    return render_template('index.html', lights=lights)


if __name__ == '__main__':
    app.run(debug=True)
