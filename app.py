from flask import Flask,request,render_template
import pickle
import json
import os
from flask import Flask ,render_template,request
import pickle
import numpy
import pandas as pd
import csv


app=Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")


@app.route('/about')
def about():
	return render_template("about.html")

@app.route("/loan",methods=["GET","POST"])
def loan():
	if request.method=="POST":
		f=None
		model=None
		try:
			f=open("loan_s_p.model","rb")
			model=pickle.load(f)
		except Exception as e:
			print("issue",e)
		finally:
			if f is not None:
				f.close()

		if model is not None:
			ai=float(request.form['ai'])
			ci=float(request.form['ci'])
			lamt=float(request.form['lamt'])
			ch=float(request.form['ch'])
			data=[ai,ci,lamt,ch]
			print(data)
			married=request.form['married']
			if married=="Yes":
				data.extend([1,0])
			else:
				data.extend([0,1])

			dependents=request.form['dependents']
			if dependents == "Zero dependents":
				data.extend([1,0,0,0])
			elif dependents == "One dependent":
				data.extend([0,1,0,0])
			elif dependents == "Two dependents":
				data.extend([0,0,1,0])
			else:
				data.extend([0,0,0,1])

			education=request.form['education']
			if education == 1:
				data.extend([1,0])
			else:
				data.extend([0,1])

			selfemp=request.form['selfemp']
			if selfemp == 1:
				data.extend([1,0])
			else:
				data.extend([0,1])

			proparea=request.form['proparea']
			if proparea == "Rural":
				data.extend([1,0,0])
			elif proparea == "SemiUrban":
				data.extend([0,1,0])
			elif proparea == "Urban":
				data.extend([0,0,1])
			
			print(data)
			
			ans=model.predict([data])
			if ans=="Y":
				msg='We are pleased to inform you that your loan is approved'
			else:
				msg='Sorry, your loan is rejected'
			msg=msg
			return render_template("loan.html",msg=msg)
		else:
			print("model issue")
			return render_template("loan.html")
	else:
		return render_template("loan.html")	

@app.route("/churn", methods=["GET" , "POST"])
def churn():
	if request.method == "POST":
		f= None
		model = None
		try:
			f=open("re.model", "rb")
			model = pickle.load(f)
		except Exception as e:
			print("Issue", e)
		finally:
			if f is not None:
				f.close()
		if model is not None:
		
			n1= float(request.form[ "n1" ])
			n2= float(request.form[ "n2" ])
			n3=float(request.form[ "n3" ])
			n4=float(request.form[ "n4" ])
			n5=float(request.form[ "n5" ])
			n6=int(request.form[ "n6" ])
			data=[n1,n2,n3,n4,n5,n6]
			print(data)
			n7=request.form["myselect"]
			if n7=="Yes":
				data.extend([1])
			else:
				data.extend([0])
			n8=request.form["myselect1"]
			if n7=="Male":
				data.extend([0,1])
			else:
				data.extend([1,0])
			
			print(data)

			ans=model.predict([data])
			if ans=='1':
				msg="HAS CHURNED"
			else:
				msg="NOT CHURNED"
			msg="Customer has: " + msg
			return render_template("churn.html",msg=msg)
		else:
			print("model issue")
			return render_template("churn.html")

	else:
		return render_template("churn.html")



@app.route("/credit",methods=["GET","POST"])

def credit():
	if request.method=="POST":
		f=None
		model=None
		try:
			f=open("CreditCard.model","rb")
			model=pickle.load(f)
		except Exception as e:
			print("Issue",e)
		finally:
			if f is not None:
				f.close()

		if model is not None:
			n1=float(request.form["n1"])
			n2=float(request.form["n2"])
			n3=float(request.form["n3"])
			n4=float(request.form["n4"])
			n5=float(request.form["n5"])
			n6=float(request.form["n6"])
			data=[n1,n2,n3,n4,n5,n6]
			print(data)
			n7=request.form["myselect"]
			if n7=="Yes":
				data.extend([1,0])
			else:
				data.extend([0,1])

			n8=request.form["myselect1"]

			if n8=="Yes":
				data.extend([1,0])
			else:
				data.extend([0,1])
			print(data)
			
			ans=model.predict([data])
			if ans=='N':
				msg="Legitimate Transaction"
			else:
				msg="Fraudulent Transaction"
			msg="Transaction is: " + msg
			return render_template("credit.html",msg=msg)
		else:
			print("model issue")
	else:
		return render_template("credit.html")
		



@app.route("/creditcsv",methods=["GET","POST"])


def creditcsv():
	if request.method=="POST":
		f=None
		model=None
		try:
			f=open("Creditcardcsv.model","rb")
			model=pickle.load(f)
		except Exception as e:
			print("Issue",e)
		finally:
			if f is not None:
				f.close()

		if model is not None:
			up_data = request.files.get('file')
			data = []
			messages = []
			i=0
			if up_data:
				for row in up_data:
					values = row.decode().strip().split(",")
					row_data = [float(val) for val in values]
					i=i+1
					data.append(row_data)
					pred = model.predict([row_data])
					print(pred)
					if pred == 0:
						msg = "Legititimate Transaction"
					else:
						msg = "Fraudulent Transaction"
					#msg = " Legitimate Transaction " if pred == '0' else  "  Fraudulent Transaction"
					messages.append(str(i)+ "]   Transaction is: " + msg + "<br>")
			return render_template("creditcsv.html", msg='\n'.join(messages))
		else:
			print("Model issue")
			return render_template("creditcsv.html", msg="Model issue")
	else:
		return render_template("creditcsv.html")
			



if __name__ == "__main__" :
	app.run(debug=False,host='0.0.0.0',use_reloader=True)











