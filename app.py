import numpy as np
from flask import Flask,request, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods= ["POST"])

def collect_values():

    import csv
    file2 = open("KnowledgeEngineExperta2.csv")
    tacos_file = list(csv.reader(file2))
    tacos_file2 = tacos_file[1:]

    rule1 = [int(i) for i in tacos_file2[0]]
    rule2 = [int(i) for i in tacos_file2[1]]
    rule3 = [int(i) for i in tacos_file2[2]]
    rule4 = [int(i) for i in tacos_file2[3]]
    rule5 = [int(i) for i in tacos_file2[4]]
    rule_values = [rule1, rule2, rule3, rule4, rule5]

    import pandas as pd
    ruledata = pd.read_csv("dataEngine.csv")
    problems = ruledata["Problem"].values
    problem_values = [i for i in problems]

    ### collect values from form
    a = request.form['name1']
    b = request.form['name2']
    c = request.form['name3']
    d = request.form['name4']
    e = request.form['name5']
    f = request.form['name6']
    g = request.form['name7']
    h = request.form['name8']
    i = request.form['name9']
    j = request.form['name10']
    final_features = [int(float(a)), int(float(b)), int(float(c)), int(float(d)), int(float(e)), int(float(f)), int(float(g)), int(float(h)), int(float(i)), int(float(j))]

    #### Rule conditions
    rule_condition_set = []
    if rule_values[0] == final_features:
        rule_condition_set.append(problem_values[0])
    elif rule_values[1] == final_features:
        rule_condition_set.append(problem_values[1])
    elif rule_values[2] == final_features:
        rule_condition_set.append(problem_values[2])
    elif rule_values[3] == final_features:
        rule_condition_set.append(problem_values[3])
    elif rule_values[4] == final_features:
        rule_condition_set.append(problem_values[4])
    else:
        rule_condition_set.append(final_features)

    #### Machine learning

    import pandas as pd
    ruledata = pd.read_csv("dataEngine.csv")
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
    predictors = ruledata.drop(columns=["Problem"], axis=1)
    target = ruledata["Problem"]
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(predictors, target, test_size=0.3)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict([final_features])

    ####### stating Problems ######

    problem_stated = [i for i in rule_condition_set]
    p = f"the probem might be : {problem_stated[0]}, please try the solutions listed below"
    for i in rule_condition_set:
        if i == problem_values[0]:
            x = """
                Step 1. Did any client join the network with a static IP address? Check to confirm all workstations network device are configured a DHCP client.
                Step 2. If you’ve just introduced a new device or server to your network, it may have its own DHCP server. Simply disable the DHCP server on that device
                """

        elif i == problem_values[1]:
            # print(i)
            x = """
                Step 1. Check to confirm network cable is properly connected at both terminals of the affected workstation and the switch/router. You may confirm this using a LAN tester.
                """

        elif i == problem_values[2]:
            # print(i)
            x = """
                Step 1. Confirm the computer is identified on the network by running ping operation on its IP address using command line.
                Step 2. Confirm NetBIOS over TCP/IP is turn on (enabled) on all computers in the workgroup.
                Step 3. Check that the Computer Browser service is started or is turned on all computers in the workgroup.
                Step 4. Ensure File and Print Sharing is installed and make sure that it is not blocked by Windows Firewall.
                """

        elif i == problem_values[3]:
            # print(i)
            x = """
                Step 1. Try rebooting the router supplying internet to the network
                Step 2. If problem persists, confirm subscription from ISP is still running. 
                Step 3. Isolate Router and test separately.
                Step 4. If problem persists, consult the ISP (Internet Service Provider)
                """

        elif i == problem_values[4]:
            # print(i)
            x = """
                Step 1. Use the command line nslookup to troubleshoot DNS problem
                """

        elif i == final_features:
            x = f"predicted problem might be {predictions}"

    #return final_features
    return render_template('home.html', problem_statement=p, rule_condition= x)
    #return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)