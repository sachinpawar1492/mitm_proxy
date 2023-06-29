from variables.variables import *
from keywords.keywords import *
from flask import Flask, request, render_template, redirect

app = Flask(__name__, static_url_path='', static_folder=get_path(static_folder), template_folder=get_path(html_folder))
app.config['JSON_SORT_KEYS'] = False  # This will prevent sorting of a JSON Keys after editing each time


# This route will serve the index.html when localhost:5000 is called.
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/proxy-server')
def proxy_server():
    hosts_apis_dict = get_data(path["hosts_apis_dict"])
    toxic_dict = get_data(path["toxic_dict"])

    return render_template('all-hosts-apis.html', non_toxic_cases=hosts_apis_dict, toxic_dict=toxic_dict)


@app.route('/block-unblock-delay', methods=['GET', 'POST'])
def block_unblock():
    toxic_dict = get_data(path["toxic_dict"])
    new_toxic_dict = toxic_dict

    delay = toxic_dict["delay_in_sec"]

    toxic_dict_path = get_path(path["toxic_dict"])

    if request.method == 'POST':
        if request.form.get('block_unblock') == 'on':
            new_toxic_dict["block"] = "True"
            if request.form.get('delay') is not None:
                delay = int(request.form.get('delay'))
            new_toxic_dict["delay_in_sec"] = delay
        else:
            new_toxic_dict["block"] = "False"
            write_data(toxic_dict_path, new_toxic_dict)

        write_data(toxic_dict_path, new_toxic_dict)

    return redirect(request.referrer)


@app.route('/update-toxic-dict', methods=['GET', 'POST'])
def update_toxic_dict():
    non_toxic_cases = get_data(path["hosts_apis_dict"])
    toxic_dict = get_data(path["toxic_dict"])
    toxic_cases = toxic_dict["toxic_cases"]
    new_toxic_dict = toxic_dict
    toxic_dict_path = get_path(path["toxic_dict"])

    if request.method == 'POST':
        for non_toxic_case in non_toxic_cases:
            for toxic_case in toxic_cases:
                checkbox_name = toxic_case + "-" + non_toxic_case
                selected_checkbox = request.form.getlist(checkbox_name)
                print(f"{checkbox_name} : {selected_checkbox}")

                new_toxic_dict["toxic_cases"][toxic_case][non_toxic_case] = selected_checkbox

        write_data(toxic_dict_path, new_toxic_dict)

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
