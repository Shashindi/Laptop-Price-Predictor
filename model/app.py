from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import os


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'), static_folder=os.path.join(os.path.dirname(__file__), '../static'))

def prediction(lst):
    filename = os.path.join(os.path.dirname(__file__), 'predictor.pickle')
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    
    pred_value = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []

        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']


        def traverse_list(lst, value, n_minus_1=False):
            
            items = lst[:-1] if n_minus_1 else lst
            for item in items:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
           

        traverse_list(company_list, company, n_minus_1=True)
        traverse_list(typename_list, typename, n_minus_1=True)
        traverse_list(opsys_list, opsys)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)

        print('Feature vector:', feature_list)
        print('Feature vector length:', len(feature_list))

        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0],2)*221
        
        
        return redirect(url_for('result', price=pred_value))

    return render_template('index.html', pred_value=pred_value)

@app.route('/result')
def result():
    price = request.args.get('price', 0)
    return render_template('result.html', pred_value=price)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
