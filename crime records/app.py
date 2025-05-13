import mysql.connector as mys
import tabulate

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/managecase")
def manage_case():
    return render_template("managecase.html")

@app.route('/result', methods=['POST'])
def result():

    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    cur.execute("SELECT A.OFFENSEID, A.DATE, A.TIME, A.DESCRIPTION, A.STATUS, B.OFFENDERID, B.NAME, B.ALIAS, B.GENDER, B.HEIGHT, B.FOUNDGUILTY, B.BLOODGROUP FROM OFFENDER_OFFENSE AS O JOIN OFFENSE A ON O.OFFENSE_ID=A.OFFENSEID JOIN OFFENDER B ON O.OFFENDER_ID=B.OFFENDERID;")
    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('result.html', results=results)


@app.route('/query12', methods=['GET','POST'])
def query12():

    val = request.form.get('options12')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    cur.execute(f"SELECT offense_id FROM (SELECT COUNT(officerid) AS number_of_officers, offense_id FROM officer GROUP BY offense_id) AS a WHERE a.number_of_officers > {val};")
    results = cur.fetchall()
    for i in range(len(results)):
        print("/t",results[i])
    cur.close()
    con.close()

    return render_template('query12.html', results=results)

@app.route('/query11', methods=['GET','POST'])
def query11():

    val = request.form.get('options11')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    cur.execute(f"SELECT w.witness_id, w.name, w.age, w.gender, o.offenseid, o.description, o.date, cp.case_id, cp.judge FROM witness w JOIN offense o ON w.offense_id = o.offenseid LEFT JOIN court_proceedings cp ON w.case_id = cp.case_id WHERE o.status = '{val}' AND (w.supports_prosecution IS NULL OR w.supports_prosecution = 0) ORDER BY o.date DESC;")
    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('query11.html', results=results)

@app.route('/query7', methods=['GET','POST'])
def query7():

    val = request.form.get('options7')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    if val=="ascending":
        cur.execute(f"SELECT off.offenseid, off.description AS Offense_Description, off.status, o.Name AS Officer_Name, o.Rank AS Officer_Rank, ofd.Name AS Offender_Name FROM offense off JOIN officer o ON off.offenseid = o.offense_id JOIN offender_offense oo ON off.offenseid = oo.offense_id JOIN offender ofd ON oo.offender_id = ofd.offenderid ORDER BY off.date;")
    else:
        cur.execute(f"SELECT off.offenseid, off.description AS Offense_Description, off.status, o.Name AS Officer_Name, o.Rank AS Officer_Rank, ofd.Name AS Offender_Name FROM offense off JOIN officer o ON off.offenseid = o.offense_id JOIN offender_offense oo ON off.offenseid = oo.offense_id JOIN offender ofd ON oo.offender_id = ofd.offenderid ORDER BY off.date DESC;")
    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('query7.html', results=results)



@app.route('/query6', methods=['GET','POST'])
def query6():

    val = request.form.get('options6')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    cur.execute(f"SELECT offender.Name AS offender_name, offense.description, offense.status FROM offender JOIN offender_offense ON offender.offenderid = offender_offense.offender_id JOIN offense ON offender_offense.offense_id = offense.offenseid WHERE offense.status = '{val}';")
    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('query6.html', results=results)

@app.route('/query5', methods=['GET','POST'])
def query5():

    val = request.form.get('options5')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    cur.execute(f"SELECT offender.Name, COUNT(offender_offense.offense_id) AS offense_count FROM offender JOIN offender_offense ON offender.offenderid = offender_offense.offender_id GROUP BY offender.Name HAVING COUNT(offender_offense.offense_id) > {val};")
    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('query5.html', results=results)

@app.route('/query4', methods=['GET','POST'])
def query4():

    val = request.form.get('options4a')
    val1 = request.form.get('options4b')
    # Example: handle Query 2 - Officers Handling Cases
    con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur=con.cursor()
    if int(val1)-int(val)<0:
        cur.execute(f"SELECT o.offenderID, o.Name, COUNT(DISTINCT off.OffenseID) AS night_offenses, GROUP_CONCAT(DISTINCT off.Description SEPARATOR ' | ') AS crime_details FROM offender o JOIN offender_offense oo ON o.offenderID = oo.offender_id JOIN offense off ON oo.offense_id = off.OffenseID WHERE HOUR(off.Time) BETWEEN {val} AND 23  OR HOUR(off.Time) BETWEEN 0 AND {val1} AND off.Status = 'Unsolved' AND o.offenderID IN (SELECT offender_id FROM offender_offense GROUP BY offender_id HAVING COUNT(*) > 1) GROUP BY o.offenderID, o.Name;")
    else:
        cur.execute(f"SELECT o.offenderID, o.Name, COUNT(DISTINCT off.OffenseID) AS night_offenses, GROUP_CONCAT(DISTINCT off.Description SEPARATOR ' | ') AS crime_details FROM offender o JOIN offender_offense oo ON o.offenderID = oo.offender_id JOIN offense off ON oo.offense_id = off.OffenseID WHERE HOUR(off.Time) BETWEEN {val} AND {val1} AND off.Status = 'Unsolved' AND o.offenderID IN (SELECT offender_id FROM offender_offense GROUP BY offender_id HAVING COUNT(*) > 1) GROUP BY o.offenderID, o.Name;")


    results = cur.fetchall()
    cur.close()
    con.close()

    return render_template('query4.html', results=results)


@app.route('/query1', methods=['POST'])
def query1():
    # Execute the SQL query
    query = """
    SELECT A.OFFENSEID, A.DATE, A.TIME, A.DESCRIPTION, A.STATUS, 
    B.OFFENDERID, B.NAME, B.ALIAS, B.GENDER, B.HEIGHT, B.FOUNDGUILTY, B.BLOODGROUP 
    FROM OFFENDER_OFFENSE AS O 
    JOIN OFFENSE A ON O.OFFENSE_ID=A.OFFENSEID 
    JOIN OFFENDER B ON O.OFFENDER_ID=B.OFFENDERID;

    """
    connection = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('query1.html', results=results)

@app.route('/query2', methods=['GET', 'POST'])
def query2():
    case_status = request.form.get('options2')
    
    
    # Connect to the database
    con = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur = con.cursor()
    if case_status == 'Unsolved':
        query = """
        SELECT off.Name, off.Specialisation,
               COUNT(o.offenseid) AS unsolved_cases
        FROM officer off
        JOIN offense o ON off.offense_id = o.offenseid
        WHERE o.Status = 'Unsolved'
        GROUP BY off.Name, off.Specialisation
        ORDER BY unsolved_cases DESC;
        """
    else:  # case_status == 'solved'
        query = """
        SELECT off.Name, off.Specialisation,
               COUNT(o.offenseid) AS solved_cases
        FROM officer off
        JOIN offense o ON off.offense_id = o.offenseid
        WHERE o.Status = 'Solved'
        GROUP BY off.Name, off.Specialisation
        ORDER BY solved_cases DESC;
        """
    
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    con.close()

    # Determine the template to render based on case status
    if case_status == 'Unsolved':
        return render_template('query2_unsolved.html', results=results)
    else:
        return render_template('query2_solved.html', results=results)
    
@app.route('/query3', methods=['GET', 'POST'])
def query3():
    verdict_status = request.form.get('options3')
    print(verdict_status, type(verdict_status))
    
    # Connect to the database
    con = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cur = con.cursor()
    
    if verdict_status == 'Guilty':
        query = """
        SELECT DISTINCT oo.offender_id, o.Name
        FROM court_proceedings cp
        JOIN offender_offense oo ON cp.offense_id = oo.offense_id
        JOIN offender o ON oo.offender_id = o.offenderID
        WHERE cp.verdict = 1;
        """
    else:  # verdict_status == 'not_guilty'
        query = """
        SELECT offenderID, Name 
        FROM offender
        WHERE offenderID NOT IN (
            SELECT DISTINCT oo.offender_id
            FROM court_proceedings cp
            JOIN offender_offense oo ON cp.offense_id = oo.offense_id
            WHERE cp.verdict = 1
        );
        """
    
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    con.close()

    # Determine the template to render based on verdict status
    if verdict_status == 'Guilty':
        return render_template('query3_guilty.html', results=results)
    else:
        return render_template('query3_notguilty.html', results=results)
    
@app.route('/query10', methods=['POST'])
def query10():
    query = """
    SELECT 
    o1.offenseid AS case_1,
    o1.description AS case_1_description,
    o2.offenseid AS case_2,
    o2.description AS case_2_description,
    GROUP_CONCAT(DISTINCT ofd.Name) AS common_offenders
FROM offense o1
JOIN offender_offense oo1 ON o1.offenseid = oo1.offense_id
JOIN offender ofd ON oo1.offender_id = ofd.offenderid
JOIN offender_offense oo2 ON ofd.offenderid = oo2.offender_id
JOIN offense o2 ON oo2.offense_id = o2.offenseid
WHERE o1.offenseid < o2.offenseid
GROUP BY o1.offenseid, o1.description, o2.offenseid, o2.description
HAVING COUNT(DISTINCT ofd.offenderid) > 0
ORDER BY case_1;
    """
    
    connection = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('query10.html', results=results)


@app.route('/query9', methods=['POST'])
def query9():
    query = """
    SELECT 
    cp.prosecutor,
    COUNT(DISTINCT cp.case_id) AS total_cases,
    SUM(CASE WHEN cp.verdict = 1 THEN 1 ELSE 0 END) AS won_cases,
    COUNT(DISTINCT w.witness_id) AS total_witnesses,
    SUM(CASE WHEN w.supports_prosecution = 1 THEN 1 ELSE 0 END) AS supporting_witnesses
FROM court_proceedings cp
LEFT JOIN witness w ON cp.case_id = w.case_id
WHERE cp.verdict IS NOT NULL
GROUP BY cp.prosecutor
ORDER BY won_cases DESC;
    """
    
    connection = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('query9.html', results=results)

@app.route('/query8', methods=['POST'])
def query8():
    query = """
    SELECT 
    o.offenderid,
    o.Name AS Offender_Name,
    off.offenseid,
    off.description AS Offense_Description,
    off.date AS Offense_Date,
    off.status,
    COUNT(w.witness_id) AS Witness_Count,
    (SELECT AVG(witness_count) 
     FROM (SELECT COUNT(witness_id) AS witness_count 
           FROM witness 
           GROUP BY offense_id) AS avg_counts) AS Average_Witness_Count
FROM offender o
JOIN offender_offense oo ON o.offenderid = oo.offender_id
JOIN offense off ON oo.offense_id = off.offenseid
JOIN witness w ON off.offenseid = w.offense_id
GROUP BY o.offenderid, o.Name, off.offenseid, off.description, off.date, off.status
HAVING COUNT(w.witness_id) > (SELECT AVG(witness_count) 
                             FROM (SELECT COUNT(witness_id) AS witness_count 
                                   FROM witness 
                                   GROUP BY offense_id) AS avg_counts)
ORDER BY Witness_Count DESC;
    """
    
    connection = mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('query8.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)






con=mys.connect(host='localhost', user='root', passwd='1106', database='crime_records')
cur=con.cursor()
cur.execute("select * from offender;")
res=cur.fetchall()
for i in range(len(res)):
    print("/t",res[i])

a="jK6jM[R7navya0311"